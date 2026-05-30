import unittest

from server_python.protocol import (
    TERMINATION_WORD,
    decode_complete_uint32_words,
    encode_uint32_words,
    strip_termination_words,
)


class ProtocolTests(unittest.TestCase):
    def test_decode_complete_words_discards_trailing_bytes(self) -> None:
        raw = encode_uint32_words([1, 2, 3]) + b"\xAA\xBB"
        words, discarded = decode_complete_uint32_words(raw)
        self.assertEqual([1, 2, 3], words)
        self.assertEqual(2, discarded)

    def test_strip_termination_words(self) -> None:
        payload, had_termination = strip_termination_words([10, TERMINATION_WORD, 20])
        self.assertEqual([10, 20], payload)
        self.assertTrue(had_termination)

    def test_encode_decode_roundtrip(self) -> None:
        original = [0, 5, 123, 999999]
        packed = encode_uint32_words(original)
        decoded, discarded = decode_complete_uint32_words(packed)
        self.assertEqual(original, decoded)
        self.assertEqual(0, discarded)


if __name__ == "__main__":
    unittest.main()
