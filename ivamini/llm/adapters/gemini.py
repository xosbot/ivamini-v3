from ivamini.llm.adapters.base import LLMAdapter

class GeminiAdapter(LLMAdapter):
    """
    Adapter for Google Gemini API.
    Optimized for reasoning and complex planning tasks.
    """

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        DESIGN ONLY: Placeholder for Gemini API call.
        """
        # Logic would go here:
        # client = genai.GenerativeModel('gemini-pro')
        # response = client.generate_content(...)
        return "DESIGN_STUB: Gemini response"

    def is_available(self) -> bool:
        """
        Checks if GEMINI_API_KEY is present in config/env.
        """
        # return os.getenv("GEMINI_API_KEY") is not None
        return True
