from pathlib import Path
from datetime import datetime

WORKSPACE_DIR = Path("ivamini/workspace")
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


class WriteFileTool:
    name = "write_file"
    permission = "WRITE"

    def execute(self, content: str):
        if not content:
            return {
                "status": "FAILURE",
                "reason": "No content provided"
            }

        filename = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = WORKSPACE_DIR / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "status": "SUCCESS",
            "file": str(file_path)
        }
