from ivamini.interface.cli import read_input
from ivamini.interface.voice import VoiceInput
from ivamini.orchestrator.core import Orchestrator
from ivamini.tools.registry import ToolRegistry
from ivamini.tools.system import GetTimeTool
from ivamini.tools.internet import WebSearchTool
from ivamini.tools.filesystem import WriteFileTool
from ivamini.config import load_config

def main():
    config = load_config()

    print("IVAmini Local System — Ready")
    print(f"Environment: {config['environment']}")

    ToolRegistry.register("get_time", GetTimeTool())
    ToolRegistry.register("web_search", WebSearchTool())
    ToolRegistry.register("write_file", WriteFileTool())

    try:
        mode, content = read_input()

        if mode == "VOICE":
            if not config["voice"]["enabled"]:
                print("Voice input disabled by config")
                return

            voice = VoiceInput()
            parsed_mode, parsed_content = voice.listen()

            if config["voice"]["require_mode"] and not parsed_mode:
                print("ERROR: MODE required in voice input")
                return

            mode = parsed_mode
            content = parsed_content

        orchestrator = Orchestrator()
        task = orchestrator.create_task(mode, mode, content)

        print("\nINTERPRETATION:")
        print(f"Task ID: {task.task_id}")
        print(f"Mode: {task.mode}")
        print(f"Type: {task.task_type}")

        print("\nPLAN:")
        if task.plan:
            for step in task.plan:
                print(f"- {step}")
        else:
            print("(No plan required)")

        print("\nPERMISSIONS:")
        print(task.permissions)

        print("\nSTATUS:")
        print(task.status)

        print("\nEXECUTION RESULT:")
        result = orchestrator.execute_task(task)
        print(result)

    except Exception as e:
        print("\nFATAL ERROR:")
        print(str(e))

if __name__ == "__main__":
    main()
