from __future__ import annotations

from pathlib import Path

from .protocol import encode_uint32_words


def sanitize_client_ip(client_ip: str) -> str:
    sanitized = client_ip.replace(":", "_").replace("%", "_").strip()
    return sanitized or "unknown_client"


def client_output_path(client_ip: str, output_dir: Path) -> Path:
    filename = f"ClientData_{sanitize_client_ip(client_ip)}.bin"
    return output_dir / filename


def append_client_words(client_ip: str, words: list[int], output_dir: Path) -> int:
    payload = encode_uint32_words(words)
    if not payload:
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    path = client_output_path(client_ip, output_dir)
    with path.open("ab") as handle:
        handle.write(payload)

    return len(payload)
