# IVA-Cortex v1.0 Model Routing Design

## Overview
This document defines the architecture for a model-agnostic routing layer. The system routes user tasks to the most appropriate Model Provider (Gemini, Groq, OpenRouter, etc.) based on the task type (PLAN, REVIEW, QUESTION) and system availability.

## Architecture

### 1. ModelRouter (`ivamini/llm/router.py`)
The central entry point for all LLM requests.
- **Responsibility**: Decides *which* provider to use.
- **Input**: `mode` (string), `prompt` (string), `metadata` (dict)
- **Output**: `text_response` (string)
- **Logic**:
  - **PLAN / REVIEW**: Routes to **Gemini** (High reasoning capability).
  - **QUESTION (Short)**: Routes to **Groq** (Low latency).
  - **Fallback**: If Gemini is unavailable, routes to **OpenRouter**.

### 2. Adapter Interface (`ivamini/llm/adapters/base.py`)
A unified interface that all providers must implement to ensure interchangeability.
- **Method**: `generate(prompt: str, system_prompt: str, **kwargs) -> str`
- **Method**: `is_available() -> bool` (Health check)

### 3. Provider Adapters (`ivamini/llm/adapters/*.py`)
Concrete implementations of the Adapter Interface.
- **GeminiAdapter**: Google Gemini API
- **GroqAdapter**: Groq LPU Inference
- **OpenRouterAdapter**: Aggregator (Fallback)
- **MistralAdapter**: Mistral AI
- **HuggingFaceAdapter**: HF Inference Endpoints

## File Structure

```
ivamini/
└── llm/
    ├── router.py              # Central Routing Logic
    ├── adapters/
    │   ├── __init__.py
    │   ├── base.py            # Abstract Base Class
    │   ├── gemini.py
    │   ├── groq.py
    │   ├── openrouter.py
    │   ├── mistral.py
    │   └── huggingface.py
    └── interface.py           # (Existing) Legacy/Placeholder
```

## Routing Rules Summary

| Task Mode | Primary Model | Fallback Model | Rationale |
| :--- | :--- | :--- | :--- |
| **PLAN** | Gemini | OpenRouter | Requires complex reasoning and long context. |
| **REVIEW** | Gemini | OpenRouter | Requires nuanced risk analysis. |
| **QUESTION** | Groq | OpenRouter | Requires speed for quick definitions. |
| **Other** | Gemini | OpenRouter | Default to high capability. |
