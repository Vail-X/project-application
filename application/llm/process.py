import openai # or anthropic/huggingface...

def process_with_llm(log_message: str) -> str:
    """Sends the log message to the LLM for structured analysis."""
    
    system_prompt = (
        "You are an expert root cause analysis assistant. Analyze the user-provided "
        "log error message. Identify the service, the probable cause, and suggest "
        "a specific action to resolve it. Respond ONLY with a structured JSON object."
    )
    
    user_prompt = f"Analyze this error log: {log_message}"
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini", # Or your preferred model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return response.choices[0].message.content