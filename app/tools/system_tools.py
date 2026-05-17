import os
import subprocess
import webbrowser
from pathlib import Path

from app.core.permissions import is_command_blocked, requires_confirmation


def open_url(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    webbrowser.open(url)

    return {
        "success": True,
        "message": f"Opened URL: {url}"
    }


def list_directory(path: str = ".") -> dict:
    target = Path(path).expanduser().resolve()

    if not target.exists():
        return {
            "success": False,
            "message": f"Path does not exist: {target}"
        }

    if not target.is_dir():
        return {
            "success": False,
            "message": f"Path is not a directory: {target}"
        }

    items = []

    for item in target.iterdir():
        items.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
            "path": str(item)
        })

    return {
        "success": True,
        "path": str(target),
        "items": items
    }


def read_file(path: str) -> dict:
    target = Path(path).expanduser().resolve()

    if not target.exists():
        return {
            "success": False,
            "message": f"File does not exist: {target}"
        }

    if not target.is_file():
        return {
            "success": False,
            "message": f"Path is not a file: {target}"
        }

    if target.name in [".env", "id_rsa", "id_ed25519"]:
        return {
            "success": False,
            "message": "Reading secret/private files is blocked."
        }

    content = target.read_text(errors="ignore")

    return {
        "success": True,
        "path": str(target),
        "content": content[:12000]
    }


def run_terminal_command(command: str, confirmed: bool = False) -> dict:
    if is_command_blocked(command):
        return {
            "success": False,
            "message": "Command blocked for safety."
        }

    if requires_confirmation(command) and not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": f"This command requires confirmation before running: {command}"
        }

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.getcwd()
        )

        return {
            "success": result.returncode == 0,
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout[-8000:],
            "stderr": result.stderr[-8000:]
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Command timed out after 30 seconds."
        }