from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import gzip
import sys
import logging

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger(__name__)

class LogEvent(BaseModel):
    message: str
    level: str
    k8s_container: str
    k8s_pod: str
    k8s_namespace: str
    k8s_app_label: str
    k8s_job_name: str
    k8s_image: str
    timestamp: str

app = FastAPI(
    title="LLM Log Analyzer Endpoint",
    description="Receives filtered ERROR logs from Vector for processing."
)

def process_with_llm(log_message: str) -> str:
    return "Process log msg: " + log_message

@app.get("/health")
async def health():
    logger.info("🏥 Health check called")
    sys.stdout.flush()  # Force flush
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_log(request: Request):
    logger.info("📨 Analyze request received")
    raw_body = await request.body()

    if request.headers.get('content-encoding') == 'gzip':
        raw_body = gzip.decompress(raw_body)

    try:
        body_json = json.loads(raw_body)
        event = LogEvent(**body_json)

        events_data = body_json if isinstance(body_json, list) else [body_json]

        results = []
        for item in events_data:
            event = LogEvent(**item)
            analysis_result = process_with_llm(event.message)

            logger.info("-" * 50)
            logger.info(f"✅ Log Received and Analyzed!")
            logger.info(f"Timestamp: {event.timestamp}")
            logger.info(f"Pod Name: {event.k8s_pod}")
            logger.info(f"Log Level: {event.level}")
            logger.info(f"Message: {event.message}")
            logger.info(f"LLM Analysis: {analysis_result}")
            logger.info("-" * 50)

            results.append({
                "status": "processed",
                "timestamp": event.timestamp,
                "analysis": analysis_result
            })

        sys.stdout.flush()

        return {"status": "ok", "results": results}

    except Exception as e:
        logger.error(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return {"status": "error", "message": str(e)}, 400

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)