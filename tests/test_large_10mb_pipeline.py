from __future__ import annotations

import os
import socket
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from server_python.manager import ServerManager


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@unittest.skipUnless(
    os.getenv("RUN_LARGE_TEST") == "1",
    "Set RUN_LARGE_TEST=1 to run the 10MB integration test.",
)
class LargePayloadPipelineTests(unittest.TestCase):
    def test_client_10mb_to_bin_and_hex(self) -> None:
        payload_size_bytes = 10 * 1024 * 1024
        word_value = 0x01020304
        word_chunk_count = 4096
        word_chunk = struct.pack("<" + "I" * word_chunk_count, *([word_value] * word_chunk_count))

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            port = _get_free_port()
            manager = ServerManager(ports=[port], output_dir=output_dir, auto_write=True)

            started = manager.start([port])
            self.assertEqual([port], started)

            try:
                with socket.create_connection(("127.0.0.1", port), timeout=10) as client:
                    bytes_sent = 0
                    while bytes_sent < payload_size_bytes:
                        remaining = payload_size_bytes - bytes_sent
                        chunk = word_chunk if remaining >= len(word_chunk) else word_chunk[:remaining]
                        client.sendall(chunk)
                        bytes_sent += len(chunk)

                    self.assertEqual(payload_size_bytes, bytes_sent)
                    client.shutdown(socket.SHUT_WR)

                bin_path = output_dir / "ClientData_127.0.0.1.bin"

                deadline = time.time() + 20.0
                while time.time() < deadline:
                    if bin_path.exists() and bin_path.stat().st_size == payload_size_bytes:
                        break
                    time.sleep(0.1)

                self.assertTrue(bin_path.exists(), "Binary output file was not created.")
                self.assertEqual(payload_size_bytes, bin_path.stat().st_size)

                hex_path = output_dir / "ClientData_127.0.0.1.txt"
                conversion = subprocess.run(
                    [
                        sys.executable,
                        "binToHex.py",
                        str(bin_path),
                        str(hex_path),
                    ],
                    cwd=str(Path(__file__).resolve().parents[1]),
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    0,
                    conversion.returncode,
                    f"stdout={conversion.stdout}\nstderr={conversion.stderr}",
                )

                self.assertTrue(hex_path.exists(), "Hex output file was not created.")

                expected_word_count = payload_size_bytes // 4
                expected_hex_size = expected_word_count * (len("04 03 02 01") + len(os.linesep))
                self.assertEqual(expected_hex_size, hex_path.stat().st_size)

                with hex_path.open("r", encoding="utf-8") as handle:
                    first_line = handle.readline().strip()

                self.assertEqual("04 03 02 01", first_line)
            finally:
                manager.stop()


if __name__ == "__main__":
    unittest.main()
