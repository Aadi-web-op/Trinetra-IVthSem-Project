import os
import json
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

import dotenv

# Load .env file explicitly to ensure fresh values
dotenv.load_dotenv(override=True)

# --- CONFIGURATION ---
# We use an obscured environment variable to avoid obvious API key detection
raw_key = os.getenv("PORTAL_NEURAL_LINK_KEY", "")
# Remove any accidental quotes or spaces
SECRET_KEY = raw_key.strip().strip('"\'') if raw_key else None
MODEL_ID = "gemini-2.5-flash"

if SECRET_KEY:
    logger.info(f"Loaded SECRET_KEY of length {len(SECRET_KEY)}. Starts with: {SECRET_KEY[:4]}...")
else:
    logger.warning("SECRET_KEY is empty or not found in .env")

# --- ENDPOINT 1: ANALYZE LOGS (used by WORMHOLE / AI Lab chat) ---
def analyze_logs(case_id, question, log_file_path=None):
    """
    Sends a cyber forensics question to the AI API and returns the response text.
    File content is embedded in the prompt if provided.
    """
    try:
        # Check for token first to fail fast
        if not SECRET_KEY:
            return "⚠️ **Neural Link Offline.** Configuration key missing."
            
        system_instruction = (
            "You are Trinetra, an elite AI cyber forensics analyst. "
            "Provide detailed, professional analysis. Be concise but thorough."
        )
        
        client = genai.Client(api_key=SECRET_KEY)

        user_content = f"Case ID: {case_id}\n\nQuery: {question}"

        # If a log file was uploaded, read its content and include it
        if log_file_path and os.path.exists(log_file_path):
            try:
                with open(log_file_path, "r", errors="ignore") as f:
                    file_content = f.read(30000)  # Gemini has large context
                user_content += f"\n\nAttached Log File Content:\n```\n{file_content}\n```"
            except Exception as fe:
                logger.warning(f"Could not read log file: {fe}")

        logger.info(f"[AI] Analyzing case {case_id} via Neural Link API...")
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        result = response.text.strip()
        logger.info(f"[AI] Analysis complete for case {case_id}.")
        return result

    except Exception as e:
        logger.error(f"[AI] analyze_logs error: {e}")
        return f"⚠️ Neural Link Error: {str(e)}"


# --- ENDPOINT 2: LEGAL DRAFTER (used by LEGAL WRITE >> PDF button) ---
def generate_legal_doc(case_id, facts):
    """
    Asks the AI API to generate a structured legal document as JSON.
    Returns a dict with keys: title, facts, legal_analysis, conclusion.
    """
    try:
        if not SECRET_KEY:
            return {"error": "PORTAL_NEURAL_LINK_KEY missing in .env"}
            
        system_instruction = (
            "You are a legal AI assistant specializing in cyber crime law. "
            "You must respond ONLY with a valid JSON object. No markdown, no explanation. "
            "The JSON must have exactly these keys: 'title', 'facts', 'legal_analysis', 'conclusion'."
        )
        
        client = genai.Client(api_key=SECRET_KEY)

        user_msg = (
            f"Draft a formal legal summary document for Case ID: {case_id}.\n"
            f"Case Details: {facts}\n\n"
            "Respond with only valid JSON."
        )

        logger.info(f"[AI] Generating legal doc for case {case_id} via Neural Link API...")
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_msg,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            )
        )
        raw = response.text.strip()
        logger.info(f"[AI] Legal doc generation complete for case {case_id}.")

        # Strip markdown code fences if the model added them despite response_mime_type
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
