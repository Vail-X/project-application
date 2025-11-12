from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import time

class LogEvent(BaseModel):
    message: str            # The core log message
    level: str              # Log severity (e.g., ERROR, WARN, FATAL)
    k8s_container: str      # Kubernetes container name
    k8s_pod: str            # Kubernetes pod name
    k8s_namespace: str      # Kubernetes namespace
    k8s_app_label: str      # Application label from K8s metadata
    k8s_job_name: str       # Job name from K8s metadata
    k8s_image: str          # Container image name
    timestamp: str          # The timestamp of the log event

app = FastAPI(
    title="LLM Log Analyzer Endpoint",
    description="Receives filtered ERROR logs from Vector for processing."
)

def process_with_llm(log_message: str) -> str:
    return "Process log msg: " + log_message

@app.post("/analyze")
async def analyze_log(request: Request):
    print("=" * 60)
    print("📥 RAW REQUEST DEBUG")
    print("=" * 60)
    print(f"Content-Type: {request.headers.get('content-type')}")
    print(f"Headers: {dict(request.headers)}")
    
    # Get raw body
    raw_body = await request.body()
    print(f"Raw Body (bytes): {raw_body}")
    print(f"Raw Body (string): {raw_body.decode('utf-8')}")
    
    try:
        body_json = await request.json()
        print(f"Parsed JSON: {json.dumps(body_json, indent=2)}")
        
        # Try to parse as LogEvent
        event = LogEvent(**body_json)
        
        analysis_result = process_with_llm(event.message)
        
        print("-" * 50)
        print(f"✅ Log Received and Analyzed!")
        print(f"Timestamp: {event.timestamp}")
        print(f"Pod Name: {event.k8s_pod}")
        print(f"Log Level: {event.level}")
        print(f"Message: {event.message}")
        print(f"LLM Analysis: {analysis_result}")
        print("-" * 50)
        
        return {"status": "ok"}
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}, 400

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)