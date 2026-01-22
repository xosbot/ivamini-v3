import ollama
import time

SYSTEM_PROMPT = """
You are IVAmini, a disciplined analytical reasoning engine.

Core principles:
- Be technically precise. Do not anthropomorphize systems.
- Clearly distinguish between human risk, system risk, and market risk.
- Do not attribute emotions or intent to algorithms.
- If a statement is probabilistic or uncertain, state that clearly.
- Prefer cause–effect explanations over generic lists.

Output rules:
- Use structured sections and bullet points.
- Avoid filler or generic advice.
- Do NOT provide financial advice or instructions.
- Focus on risks, tradeoffs, and implications only.

Your purpose is to support:
- Strategic thinking
- Risk analysis
- System design reasoning
- Decision clarity under uncertainty
"""

class LocalLLM:
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model

    def analyze(self, prompt: str) -> dict:
        start_time = time.time()
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]
        )

        content = response["message"]["content"].strip()
        duration_ms = int((time.time() - start_time) * 1000)

        return {
            "status": "SUCCESS",
            "summary": content[:400],
            "confidence": "LOCAL_LLM_OLLAMA_LLAMA3_1B",
            "raw_output": content,
            "duration_ms": duration_ms
        }
