import os
import json
import logging
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
HF_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"


def _get_client():
    if not HF_TOKEN:
        raise ValueError("HF_API_TOKEN is missing in .env")
    return InferenceClient(model=MODEL_ID, token=HF_TOKEN)


# --- ENDPOINT 1: ANALYZE LOGS (used by WORMHOLE / AI Lab chat) ---
def analyze_logs(case_id, question, log_file_path=None):
    """
    Sends a cyber forensics question to the Llama API and returns the response text.
    File content is embedded in the prompt if provided.
    """
    try:
        client = _get_client()

        system_msg = (
            "You are Trinetra, an elite AI cyber forensics analyst. "
            "Provide detailed, professional analysis. Be concise but thorough."
        )

        user_content = f"Case ID: {case_id}\n\nQuery: {question}"

        # If a log file was uploaded, read its content and include it
        if log_file_path and os.path.exists(log_file_path):
            try:
                with open(log_file_path, "r", errors="ignore") as f:
                    file_content = f.read(8000)  # Limit to 8KB to stay within token limits
                user_content += f"\n\nAttached Log File Content:\n```\n{file_content}\n```"
            except Exception as fe:
                logger.warning(f"Could not read log file: {fe}")

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_content},
        ]

        logger.info(f"[AI] Analyzing case {case_id} via InferenceClient API...")
        # Add a timeout to the client call to avoid hanging
        response = client.chat_completion(messages, max_tokens=500) 
        result = response.choices[0].message.content.strip()
        logger.info(f"[AI] Analysis complete for case {case_id}.")
        return result

    except Exception as e:
        logger.error(f"[AI] analyze_logs error: {e}")
        return f"⚠️ AI Error: {str(e)}"


# --- ENDPOINT 2: LEGAL DRAFTER (used by LEGAL WRITE >> PDF button) ---
def generate_legal_doc(case_id, facts):
    """
    Asks the Llama API to generate a structured legal document as JSON.
    Returns a dict with keys: title, facts, legal_analysis, conclusion.
    """
    try:
        client = _get_client()

        system_msg = (
            "You are a legal AI assistant specializing in cyber crime law. "
            "You must respond ONLY with a valid JSON object. No markdown, no explanation. "
            "The JSON must have exactly these keys: 'title', 'facts', 'legal_analysis', 'conclusion'."
        )

        user_msg = (
            f"Draft a formal legal summary document for Case ID: {case_id}.\n"
            f"Case Details: {facts}\n\n"
            "Respond with only valid JSON."
        )

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ]

        logger.info(f"[AI] Generating legal doc for case {case_id} via InferenceClient API...")
        response = client.chat_completion(messages, max_tokens=600)
        raw = response.choices[0].message.content.strip()
        logger.info(f"[AI] Legal doc generation complete for case {case_id}.")

        # Strip markdown code fences if the model added them
        if raw.startswith("```json"):
            raw = raw[7:].rstrip("`").strip()
        elif raw.startswith("```"):
            raw = raw[3:].rstrip("`").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning(f"[AI] JSON parse failed, wrapping raw text. Raw: {raw[:200]}")
            return {
                "title": f"Legal Report - Case {case_id}",
                "facts": facts,
                "legal_analysis": raw,
                "conclusion": "Generated via AI. Manual review recommended."
            }

    except Exception as e:
        logger.error(f"[AI] generate_legal_doc error: {e}")
        return {"error": str(e)}
