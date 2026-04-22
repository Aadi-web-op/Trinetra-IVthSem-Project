import os
from . import ai_service
import tempfile
import logging

logger = logging.getLogger(__name__)

class TrinetraAI:
    @staticmethod
    def process_query(query, user_context=None, attachment=None, case_id=None):
        """
        Main entry point for AI processing.
        """
        response_text = ""
        
        # Default ID if none provided
        if not case_id:
             case_id = f"CMD-USER-{user_context.get('id', '000')}" if user_context else "CMD-GUEST"

        # --- REMOTE ANALYSIS (Hugging Face) ---
        try:
            temp_path = None
            if attachment:
                # Handle File Upload
                suffix = os.path.splitext(attachment.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    for chunk in attachment.chunks():
                        tmp.write(chunk)
                    temp_path = tmp.name

            # Call the Service
            response_text = ai_service.analyze_logs(case_id, query, temp_path)
            
            # Clean up temp file
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

            if response_text:
                 return response_text

        except Exception as e:
             logger.error(f"Remote AI Failed: {e}")

        # --- FALLBACK (If AI is offline) ---
        return "⚠️ **Neural Link Offline.** Check Hugging Face Space status."
    
    @staticmethod
    def generate_legal_doc(case_id, justification):
        return ai_service.generate_legal_doc(case_id, justification)
