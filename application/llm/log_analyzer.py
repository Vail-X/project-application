from fastapi import FastAPI, Request, HTTPException
import json
import gzip
import sys
import logging
import asyncio
import time
from datetime import datetime

from llm_processor import LogEvent, process_with_llm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger(__name__)

MAX_LLM_CONCURRENCY = 5
llm_semaphore = asyncio.Semaphore(MAX_LLM_CONCURRENCY)

PROCESSED_FINGERPRINTS = {}
CACHE_EXPIRY_SECONDS = 600
CLEANUP_INTERVAL_SECONDS = 300

async def throttled_process(event: LogEvent):
    """Acquires the semaphore before executing the synchronous LLM call."""
    async with llm_semaphore:
        return await asyncio.to_thread(process_with_llm, event)

def get_fingerprint(event: LogEvent):
    """Creates a unique key for deduplication based on service and error message."""
    message_key = event.message[:50]
    return f"{event.k8s_app_label}:{message_key}"

def cleanup_fingerprint_cache():
    """Removes expired fingerprints from the in-memory cache."""
    current_time = time.time()
    keys_to_delete = []

    for fingerprint, expiry_time in PROCESSED_FINGERPRINTS.items():
        if expiry_time < current_time:
            keys_to_delete.append(fingerprint)

    for key in keys_to_delete:
        del PROCESSED_FINGERPRINTS[key]

    logger.info(f"🧹 Cleaned up {len(keys_to_delete)} expired fingerprints. Cache size: {len(PROCESSED_FINGERPRINTS)}")

async def background_cache_cleanup():
    """Runs the cleanup function periodically."""
    while True:
        cleanup_fingerprint_cache()
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)

# --- FastAPI App Setup ---

app = FastAPI(
    title="LLM Log Analyzer Endpoint",
    description="Receives filtered ERROR logs from Vector for processing."
)

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(background_cache_cleanup())

@app.get("/health")
async def health():
    logger.info("🏥 Health check called")
    sys.stdout.flush()
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_log(request: Request):
    raw_body_bytes = await request.body()
    if request.headers.get('content-encoding') == 'gzip':
        try:
            raw_body_str = gzip.decompress(raw_body_bytes).decode('utf-8')
        except OSError as e:
            logger.error(f"Gzip decompression failed: {e}")
            raise HTTPException(status_code=400, detail="Gzip decompression failed or bad data.")
    else:
        raw_body_str = raw_body_bytes.decode('utf-8')

    try:
        body_json = json.loads(raw_body_str)
        events_data = body_json if isinstance(body_json, list) else [body_json]

        analysis_tasks = []
        logs_to_process = []
        current_time = time.time()

        for item in events_data:
            event = LogEvent(**item)
            fingerprint = get_fingerprint(event)

            if fingerprint in PROCESSED_FINGERPRINTS and current_time < PROCESSED_FINGERPRINTS[fingerprint]:
                logger.info(f"⏭️ Skipping duplicate log from {event.k8s_app_label} (Cached until {datetime.fromtimestamp(PROCESSED_FINGERPRINTS[fingerprint]).strftime('%H:%M:%S')})")
                continue

            PROCESSED_FINGERPRINTS[fingerprint] = current_time + CACHE_EXPIRY_SECONDS
            logs_to_process.append(event)

            task = asyncio.create_task(throttled_process(event))
            analysis_tasks.append(task)

        logger.info(f"Received {len(events_data)} logs. Processing {len(analysis_tasks)} unique logs.")

        if not analysis_tasks:
            sys.stdout.flush()
            return {"status": "ok", "message": f"All {len(events_data)} logs were duplicates and skipped."}

        results_data = await asyncio.gather(*analysis_tasks)

        for event, analysis_result_json_str in zip(logs_to_process, results_data):
            cleaned_str = analysis_result_json_str.strip()
            if cleaned_str.startswith("```json"):
                cleaned_str = cleaned_str.strip('`').lstrip('json').strip()

            try:
                analysis_result = json.loads(cleaned_str)
            except json.JSONDecodeError as e:
                logger.error(f"LLM output error (Bad JSON) for pod {event.k8s_pod}: {e}. Raw: {analysis_result_json_str[:150]}...")
                analysis_result = {
                    "service_affected": event.k8s_app_label,
                    "probable_cause": "LLM returned unparseable JSON output. See server logs for raw response.",
                    "suggested_action": "Check LLM service status and refine system prompt for strict JSON adherence."
                }

            logger.info("-" * 50)
            logger.info(f"Timestamp: {event.timestamp}")
            logger.info(f"Pod Name: {event.k8s_pod}")
            logger.info(f"Message: {event.message}")
            logger.info(f"LLM Affect: {analysis_result.get('service_affected')}")
            logger.info(f"LLM Cause: {analysis_result.get('probable_cause')}")
            logger.info(f"LLM Suggestion: {analysis_result.get('suggested_action')}")
            logger.info("-" * 50)

        sys.stdout.flush()

        return {"status": "ok", "message": f"Successfully processed {len(events_data)} log events."}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in request body.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)