import tempfile
import unittest
from pathlib import Path

from server_python.manager import ServerManager


class ManagerSmokeTests(unittest.TestCase):
    def test_transfer_buffered_data_no_buffer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manager = ServerManager(ports=[5501], output_dir=Path(tmp_dir), auto_write=False)
            bytes_written = manager.transfer_buffered_data("127.0.0.1")
            self.assertEqual(0, bytes_written)


if __name__ == "__main__":
    unittest.main()
