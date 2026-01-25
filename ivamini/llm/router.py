from ivamini.llm.adapters.gemini import GeminiAdapter

class ModelRouter:
    """
    Minimal Routing Layer for IVA-Cortex v1.0.
    Routes ALL requests to Gemini.
    """

    def __init__(self):
        # Initialize only Gemini as per constraints
        self.gemini = GeminiAdapter()

    def route(self, mode: str, prompt: str, system_prompt: str = None, metadata: dict = None) -> dict:
        """
        Routes the request to Gemini.
        Returns a dictionary to match the expected interface of AnalysisAgent/Orchestrator.
        """
        # Strict routing: Always Gemini
        import time
        start_time = time.time()

        raw_response = self.gemini.generate(prompt, system_prompt=system_prompt)

        duration_ms = int((time.time() - start_time) * 1000)

        # Check for error prefix from adapter
        status = "SUCCESS"
        if raw_response.startswith("ERROR:"):
            status = "ERROR"
            # If error, the raw_response is the error message
            error_msg = raw_response
            summary = ""
        else:
            summary = raw_response

        # Return format must match what AnalysisAgent/Orchestrator expects
        # previously LocalLLM returned:
        # { "status": ..., "summary": ..., "confidence": ..., "raw_output": ..., "duration_ms": ... }

        return {
            "status": status,
            "summary": summary,  # The actual content
            "error": raw_response if status == "ERROR" else None,
            "confidence": "GEMINI_PRO",
            "raw_output": raw_response,
            "duration_ms": duration_ms
        }
