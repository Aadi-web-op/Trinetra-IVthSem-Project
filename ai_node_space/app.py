import gradio as gr
import json
import time
import os
import datetime
import google.generativeai as genai

import dotenv

dotenv.load_dotenv(override=True)

# --- CONFIGURATION ---
raw_key = os.getenv("PORTAL_NEURAL_LINK_KEY", "")
SECRET_KEY = raw_key.strip().strip('"\'') if raw_key else None
MODEL_ID = "gemini-2.5-flash"

if SECRET_KEY:
    print(f"Loaded SECRET_KEY of length {len(SECRET_KEY)}. Starts with: {SECRET_KEY[:4]}...")
else:
    print("SECRET_KEY is empty or not found in .env")

def _get_model(system_instruction):
    if not SECRET_KEY:
        return None
    genai.configure(api_key=SECRET_KEY)
    return genai.GenerativeModel(
        model_name=MODEL_ID,
        system_instruction=system_instruction
    )

# --- LOGIC 1: UNIVERSAL FILE ANALYZER ---
def process_file(file_obj, user_question):
    if not user_question: user_question = "General Analysis"
    
    if not SECRET_KEY:
        return "⚠️ Neural Link Offline. PORTAL_NEURAL_LINK_KEY missing.", {"status": "error"}

    try:
        model = _get_model("You are Trinetra, an elite cyber forensics AI.")
        user_content = f"Query: {user_question}"

        if file_obj and os.path.exists(file_obj.name):
            with open(file_obj.name, "r", errors="ignore") as f:
                content = f.read(30000)
            user_content += f"\n\nAttached File:\n```\n{content}\n```"

        response = model.generate_content(user_content)
        ai_answer = response.text.strip()
    except Exception as e:
        ai_answer = f"Error: {str(e)}"

    db_data = {
        "analysis_type": "Security Scan",
        "timestamp": time.time(),
        "summary": "Processed via Neural Link"
    }
    return ai_answer, db_data

# --- LOGIC 2: LEGAL DRAFTING ---
def draft_legal_doc(case_id, justification):
    if not SECRET_KEY:
        return {"error": "PORTAL_NEURAL_LINK_KEY missing in environment"}

    try:
        model = _get_model(
            "You are a legal AI. Respond ONLY with valid JSON with keys: title, facts, legal_analysis, conclusion."
        )
        user_content = f"Draft legal doc for case: {case_id}.\nFacts: {justification}"

        response = model.generate_content(
            user_content,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        raw = response.text.strip()
        
        if raw.startswith("```json"):
            raw = raw[7:].rstrip("`").strip()
        elif raw.startswith("```"):
            raw = raw[3:].rstrip("`").strip()
            
        return json.loads(raw)
    except Exception as e:
        return {
            "title": "ERROR DRAFTING",
            "facts": justification,
            "legal_analysis": str(e),
            "conclusion": "FAILED"
        }

# --- LOGIC 3: CASE MANAGER ---
def fetch_or_create_case(case_no, justification):
    """
    Simple endpoint to accept case sync / keep-alive pings
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"acknowledged: {case_no} at {timestamp}"

# --- THE INTERFACE ---
with gr.Blocks() as demo:
    gr.Markdown("# Trinetra AI Node")
    
    with gr.Tab("Universal_Analyzer"):
        in_file = gr.File()
        in_text = gr.Textbox()
        out_text = gr.Textbox()
        out_json = gr.JSON()
        btn_logs = gr.Button("Analyze")
        btn_logs.click(process_file, inputs=[in_file, in_text], outputs=[out_text, out_json], api_name="analyze_logs")

    with gr.Tab("Legal_Drafter"):
        in_case = gr.Textbox()
        in_just = gr.Textbox()
        out_doc = gr.JSON()
        btn_legal = gr.Button("Draft")
        btn_legal.click(draft_legal_doc, inputs=[in_case, in_just], outputs=out_doc, api_name="draft_legal_json")

    with gr.Tab("Case_Manager"):
        in_c_case = gr.Textbox()
        in_c_just = gr.Textbox()
        out_c_res = gr.Textbox()
        btn_case = gr.Button("Sync Case")
        btn_case.click(fetch_or_create_case, inputs=[in_c_case, in_c_just], outputs=out_c_res, api_name="fetch_or_create_case")

demo.queue()
demo.launch(server_name="0.0.0.0", server_port=7860)
