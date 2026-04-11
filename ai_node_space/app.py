import gradio as gr
import json
import time
import os
import datetime

# --- LOGIC 1: UNIVERSAL FILE ANALYZER ---
def process_file(file_obj, user_question):
    # (Keep your existing logic, just ensuring safety)
    if not user_question: user_question = "General Analysis"
    
    ai_answer = f"[Analysis] Processing query: {user_question}. No threats detected in simulated scan."
    if file_obj:
        ai_answer += f" File '{os.path.basename(file_obj.name)}' processed."
        
    db_data = {
        "analysis_type": "Security Scan",
        "timestamp": time.time(),
        "summary": ai_answer
    }
    return ai_answer, db_data

# --- LOGIC 2: LEGAL DRAFTING ---
def draft_legal_doc(case_id, justification):
    # (Keep your existing logic)
    legal_text = f"The justification '{justification}' is valid under Section 4."
    doc_structure = {
        "case_id": case_id,
        "title": "OFFICIAL LEGAL JUSTIFICATION",
        "facts": justification,
        "analysis": legal_text,
        "conclusion": "APPROVED",
        "date": time.strftime("%d-%b-%Y")
    }
    return doc_structure

# --- LOGIC 3: CASE MANAGER (MISSING IN YOUR CODE - ADDED HERE) ---
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
        # Matches ai_service 'analyze_logs'
        btn_logs.click(process_file, inputs=[in_file, in_text], outputs=[out_text, out_json], api_name="analyze_logs")

    with gr.Tab("Legal_Drafter"):
        in_case = gr.Textbox()
        in_just = gr.Textbox()
        out_doc = gr.JSON()
        btn_legal = gr.Button("Draft")
        # Matches ai_service 'generate_legal_doc'
        btn_legal.click(draft_legal_doc, inputs=[in_case, in_just], outputs=out_doc, api_name="draft_legal_json")

    with gr.Tab("Case_Manager"):
        in_c_case = gr.Textbox()
        in_c_just = gr.Textbox()
        out_c_res = gr.Textbox()
        btn_case = gr.Button("Sync Case")
        # Matches ai_service 'fetch_or_create_case'
        btn_case.click(fetch_or_create_case, inputs=[in_c_case, in_c_just], outputs=out_c_res, api_name="fetch_or_create_case")

demo.queue()
demo.launch(server_name="0.0.0.0", server_port=7860)
