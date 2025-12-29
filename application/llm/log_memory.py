import asyncio
import time
import logging
from llm_processor import LogEvent, process_with_llm

MAX_LLM_CONCURRENCY = 5
llm_semaphore = asyncio.Semaphore(MAX_LLM_CONCURRENCY)

PROCESSED_FINGERPRINTS = {}
CACHE_EXPIRY_SECONDS = 600
CLEANUP_INTERVAL_SECONDS = 300

logger = logging.getLogger(__name__)

async def throttled_process(event: LogEvent):
    """Acquires the semaphore before executing the synchronous LLM call."""
    async with llm_semaphore:
        return await asyncio.to_thread(process_with_llm, event)

def get_fingerprint(event: LogEvent):
    """Creates a unique key for deduplication based on service and error message."""
    message_key = event.message[:50]
    logger.info(f"Finger {event.message[:50]}")
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