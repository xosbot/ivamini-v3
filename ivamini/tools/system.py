from datetime import datetime

class GetTimeTool:

    name = "get_time"
    permission = "READ"

    def execute(self):
        return {
            "status": "SUCCESS",
            "output": datetime.now().isoformat()
        }
