from app.tools.system_tools import (
    open_url,
    list_directory,
    read_file,
    run_terminal_command,
)


class ToolRegistry:

    def __init__(self):
        self.tools = {
            "open_url": open_url,
            "list_directory": list_directory,
            "read_file": read_file,
            "run_terminal_command": run_terminal_command,
        }

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": "open_url",
                "description": "Open a website URL in the default browser.",
                "example": {"url": "https://google.com"}
            },
            {
                "name": "list_directory",
                "description": "List files and folders in a directory.",
                "example": {"path": "~/Downloads"}
            },
            {
                "name": "read_file",
                "description": "Read a local file content safely.",
                "example": {"path": "~/test.txt"}
            },
            {
                "name": "run_terminal_command",
                "description": "Run a terminal command safely.",
                "example": {"command": "git status", "confirmed": False}
            }
        ]

    def execute(self, tool_name: str, tool_input: dict) -> dict:
        tool = self.tools.get(tool_name)

        if not tool:
            return {
                "success": False,
                "message": f"Unknown tool: {tool_name}"
            }

        return tool(**tool_input)