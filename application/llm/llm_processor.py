# llm_processor.py

import os
import logging
from pydantic import BaseModel, Field
from huggingface_hub import InferenceClient

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

class AnalysisResult(BaseModel):
    """Defines the structured JSON output expected from the LLM."""
    service_affected: str = Field(..., description="The name of the service or component affected.")
    probable_cause: str = Field(..., description="A concise explanation of the most likely root cause.")
    suggested_action: str = Field(..., description="A specific, actionable step to resolve the issue.")

client = InferenceClient(api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

def process_with_llm(event: LogEvent) -> str:
    system_prompt = (
        "You are an expert root cause analysis assistant. Analyze the provided log event metadata "
        "and the error message. Identify the service, the probable cause, and suggest "
        "a specific action to resolve it. "
        "Respond **STRICTLY AND ONLY** with a structured JSON object conforming to the following keys: "
        "'service_affected', 'probable_cause', and 'suggested_action'. **DO NOT** include any markdown, commentary, or text outside the JSON object itself."
    )

    user_prompt = f"""
    Analyze this error log event and its full Kubernetes context. Identify the service, cause, and action.

    Kubernetes Context:
    - **App Label (Service):** {event.k8s_app_label}
    - **Namespace:** {event.k8s_namespace}
    - **Pod Name:** {event.k8s_pod}
    - **Container:** {event.k8s_container}
    - **Image Version:** {event.k8s_image}
    - **Job/Cron Name (if present):** {event.k8s_job_name}
    - **Timestamp (Start of Event):** {event.timestamp}

    Error Message:
    ---
    {event.message}
    ---
    """

    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_key:
        logger.error("HUGGINGFACEHUB_API_TOKEN environment variable not set.")
        return AnalysisResult(
            service_affected="System",
            probable_cause="API Key Missing",
            suggested_action="Set HUGGINGFACEHUB_API_TOKEN environment variable."
        ).model_dump_json()

    try:
        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Thinking",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format={"type": "json_object"}
        )

        return completion.choices[0].message.content

    except Exception as e:
        logger.error(f"Error during LLM API call: {e}")
        return AnalysisResult(
            service_affected="LLM Service",
            probable_cause="LLM API call failed",
            suggested_action=f"Check network/LLM service health. Error: {str(e)}"
        ).model_dump_json()