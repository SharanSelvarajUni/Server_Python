from __future__ import annotations

import struct
from typing import Iterable

TERMINATION_WORD = 0xFFFFFFFF


def decode_complete_uint32_words(raw_data: bytes) -> tuple[list[int], int]:
    """Decode complete uint32 words and report discarded trailing bytes."""
    complete_bytes = len(raw_data) - (len(raw_data) % 4)
    discarded = len(raw_data) - complete_bytes

    if complete_bytes == 0:
        return [], discarded

    words = list(struct.unpack(f"<{complete_bytes // 4}I", raw_data[:complete_bytes]))
    return words, discarded


def strip_termination_words(words: Iterable[int]) -> tuple[list[int], bool]:
    """Remove termination markers from payload and signal if any were found."""
    had_termination = False
    payload: list[int] = []

    for word in words:
        if word == TERMINATION_WORD:
            had_termination = True
            continue
        payload.append(word)

    return payload, had_termination


def encode_uint32_words(words: Iterable[int]) -> bytes:
    values = list(words)
    if not values:
        return b""
    return struct.pack(f"<{len(values)}I", *values)
