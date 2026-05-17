import json
from pathlib import Path

from app.llm.ollama_provider import OllamaProvider
from app.core.tool_registry import ToolRegistry


class AssistantOrchestrator:

    def __init__(self):
        self.llm = OllamaProvider()
        self.tools = ToolRegistry()
        self.system_prompt = self.load_system_prompt()

    def load_system_prompt(self) -> str:
        prompt_path = Path("app/prompts/system_prompt.txt")
        return prompt_path.read_text()

    async def chat(self, user_message: str) -> dict:
        tool_decision = await self.decide_tool(user_message)

        if tool_decision.get("needs_tool"):
            tool_name = tool_decision.get("tool_name")
            tool_input = tool_decision.get("tool_input", {})

            tool_result = self.tools.execute(tool_name, tool_input)

            final_answer = await self.generate_final_answer(
                user_message=user_message,
                tool_decision=tool_decision,
                tool_result=tool_result
            )

            return {
                "mode": "tool",
                "tool_decision": tool_decision,
                "tool_result": tool_result,
                "answer": final_answer
            }

        answer = await self.llm.chat([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ])

        return {
            "mode": "chat",
            "answer": answer
        }

    async def decide_tool(self, user_message: str) -> dict:
        tools_json = json.dumps(self.tools.list_tools(), indent=2)

        prompt = f"""
You are a tool decision engine.

Available tools:
{tools_json}

User request:
{user_message}

Decide if a tool is needed.

Return JSON only in this format:
{{
  "needs_tool": true,
  "tool_name": "tool name here",
  "tool_input": {{}},
  "reason": "why tool is needed"
}}

Rules:
- If user asks to open a website, use open_url.
- If user asks to list files/folders, use list_directory.
- If user asks to read a file, use read_file.
- If user asks to run/check terminal command, use run_terminal_command.
- If no tool is needed, return:
{{
  "needs_tool": false,
  "tool_name": null,
  "tool_input": {{}},
  "reason": "No tool needed"
}}
"""

        response = await self.llm.chat([
            {"role": "system", "content": "You return valid JSON only. No markdown."},
            {"role": "user", "content": prompt}
        ])

        try:
            return json.loads(response)
        except Exception:
            return {
                "needs_tool": False,
                "tool_name": None,
                "tool_input": {},
                "reason": "Could not parse tool decision."
            }

    async def generate_final_answer(
        self,
        user_message: str,
        tool_decision: dict,
        tool_result: dict
    ) -> str:
        prompt = f"""
User asked:
{user_message}

Tool decision:
{json.dumps(tool_decision, indent=2)}

Tool result:
{json.dumps(tool_result, indent=2)}

Now answer the user clearly.
If the tool failed, explain the failure.
If confirmation is required, ask the user to confirm.
"""

        return await self.llm.chat([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ])