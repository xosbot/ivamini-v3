from ivamini.llm.adapters.base import LLMAdapter
import os
import requests
import json

class GeminiAdapter(LLMAdapter):
    """
    Adapter for Google Gemini API via REST.
    Uses 'gemini-pro' model.
    """

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        Sends prompt to Gemini API.
        """
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return "ERROR: GEMINI_API_KEY not found in environment variables."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        # Construct payload
        # Gemini API expects: {"contents": [{"parts": [{"text": "..."}]}]}
        # If system_prompt is provided, we prepend it (REST API doesn't have distinct system role in v1beta easily without chat history structure, keeping it simple as requested)

        full_text = prompt
        if system_prompt:
            full_text = f"System Instruction: {system_prompt}\n\nUser Input: {prompt}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": full_text
                }]
            }]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            # Extract text
            # Response format: candidates[0].content.parts[0].text
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
            except (KeyError, IndexError):
                return f"ERROR: Unexpected response format from Gemini: {json.dumps(data)}"

        except requests.exceptions.RequestException as e:
            return f"ERROR: Gemini API Request Failed: {str(e)}"

    def is_available(self) -> bool:
        """
        Checks if GEMINI_API_KEY is present.
        """
        return bool(os.environ.get("GEMINI_API_KEY"))
