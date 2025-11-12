from fastapi import FastAPI
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
async def analyze_log(event: LogEvent):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)