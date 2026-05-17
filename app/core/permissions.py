import re


BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    r"sudo\s+rm",
    r"mkfs",
    r"dd\s+if=",
    r":\(\)\{",
    r"chmod\s+-R\s+777\s+/",
    r"chown\s+-R",
    r"shutdown",
    r"reboot",
    r"curl\s+.*\|\s*sh",
    r"wget\s+.*\|\s*sh",
]


def is_command_blocked(command: str) -> bool:
    command_lower = command.lower().strip()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command_lower):
            return True

    return False


def requires_confirmation(command: str) -> bool:
    risky_keywords = [
        "sudo",
        "apt install",
        "apt remove",
        "pip install",
        "npm install",
        "git push",
        "git commit",
        "rm ",
        "mv ",
        "cp ",
        "chmod",
        "chown",
    ]

    command_lower = command.lower()

    return any(keyword in command_lower for keyword in risky_keywords)