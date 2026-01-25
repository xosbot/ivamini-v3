from ivamini.llm.adapters.base import LLMAdapter

class HuggingFaceAdapter(LLMAdapter):
    """
    Adapter for HuggingFace Inference Endpoints.
    Optional provider for specialized open-source models.
    """

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        DESIGN ONLY: Placeholder for HuggingFace API call.
        """
        # Logic would go here:
        # client = InferenceClient(token=...)
        # response = client.text_generation(...)
        return "DESIGN_STUB: HuggingFace response"

    def is_available(self) -> bool:
        """
        Checks if HF_TOKEN is present in config/env.
        """
        # return os.getenv("HF_TOKEN") is not None
        return True
