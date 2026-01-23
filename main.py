import os
from ivamini.interface.cli import read_input
from ivamini.orchestrator.core import Orchestrator
from ivamini.tools.registry import ToolRegistry
from ivamini.tools.system import GetTimeTool
from ivamini.tools.internet import WebSearchTool
from ivamini.tools.filesystem import WriteFileTool
from ivamini.config import load_config

def main():
    config = load_config()

    print("IVAmini Local System — Ready")
    if config.get("dry_mode"):
        print("System Mode: DRY RUN (LLM Inference Disabled)")
    print(f"Environment: {config['environment']}")
    print(f"Config File: {os.path.abspath('config.json')}")

    # Traceability: Show active model to help debug infrastructure errors
    model_name = config.get('llm', {}).get('model', 'Unknown')
    print(f"LLM Model:   {model_name}")

    if "tiny" in model_name.lower():
        print("             (Running in Low-Resource Compatibility Mode)")

    ToolRegistry.register("get_time", GetTimeTool())
    # SAFETY: Disabled for v1.0-local (Reasoning Only / Local Scope)
    # ToolRegistry.register("web_search", WebSearchTool())
    # ToolRegistry.register("write_file", WriteFileTool())

    try:
        mode, content = read_input()

        if mode == "VOICE":
            if not config["voice"]["enabled"]:
                print("Voice input disabled by config")
                return

            from ivamini.interface.voice import VoiceInput
            voice = VoiceInput()
            parsed_mode, parsed_content = voice.listen()

            if config["voice"]["require_mode"] and not parsed_mode:
                print("ERROR: MODE required in voice input")
                return

            mode = parsed_mode
            content = parsed_content

        orchestrator = Orchestrator(config)
        task = orchestrator.create_task(mode, mode, content)

        print("\nINTERPRETATION:")
        print(f"Task ID: {task.task_id}")
        print(f"Mode: {task.mode}")
        print(f"Type: {task.task_type}")

        print("\nEXECUTION RESULT:")
        result = orchestrator.execute_task(task)

        if result.get("status") == "ERROR":
            payload = result.get("result", {})
            error_msg = payload.get("error") if isinstance(payload, dict) else str(payload)
            print(f"❌ FAILED: {error_msg}")

            if "connection failed" in str(error_msg).lower() or "500" in str(error_msg):
                print("\n   [!] INFRASTRUCTURE ERROR")
                print("   1. Ensure Ollama is running ('ollama serve')")
                print("   2. Check available RAM/VRAM")
                print("   3. If persistent, enable 'dry_mode': true in config.json")
                if "exit status 2" in str(error_msg):
                    print("   3. Model file corrupt? Try: 'ollama rm <model> && ollama pull <model>'")
                    print("   4. Hardware incompatible? Try switching model to 'tinyllama' in config.json")
        else:
            print("\nRESPONSE:")
            print(result.get("result", "No content returned."))
            print("-" * 40)
            print(f"Status: {result.get('status')} | Duration: {result.get('duration_ms', 0)}ms")

    except Exception as e:
        print("\nFATAL ERROR:")
        print(str(e))

if __name__ == "__main__":
    main()
