from __future__ import annotations

import argparse
import cmd
import logging
import shlex
import signal
from pathlib import Path

from .manager import ServerManager


def _command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="server-cli", add_help=True)
    parser.add_argument("--ports", nargs="+", type=int, default=[5001, 5002, 5003, 5004])
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--manual-transfer-only", action="store_true")
    return parser


class ServerShell(cmd.Cmd):
    intro = "Server CLI ready. Type help or ? to list commands."
    prompt = "server> "

    def __init__(self, manager: ServerManager, default_ports: list[int]) -> None:
        super().__init__()
        self.manager = manager
        self.default_ports = default_ports

    def do_start(self, arg: str) -> None:
        parser = argparse.ArgumentParser(prog="start", add_help=False)
        parser.add_argument("--ports", nargs="+", type=int)

        try:
            parsed = parser.parse_args(shlex.split(arg))
        except SystemExit:
            print("Usage: start [--ports 5001 5002 ...]")
            return

        ports = parsed.ports if parsed.ports else self.default_ports
        started = self.manager.start(ports=ports)

        if not started:
            print("Server is already running.")
            return

        print(f"Started servers on ports: {', '.join(str(port) for port in started)}")

    def do_stop(self, arg: str) -> None:
        _ = arg
        if not self.manager.is_running():
            print("Server is not running.")
            return
        self.manager.stop()
        print("All servers stopped.")

    def do_list(self, arg: str) -> None:
        _ = arg
        rows = self.manager.list_clients()
        if not rows:
            print("No clients tracked.")
            return

        print("Client IP\tPort\tStatus")
        for client_ip, port, status in rows:
            print(f"{client_ip}\t{port}\t{status}")

    def do_send(self, arg: str) -> None:
        parser = argparse.ArgumentParser(prog="send", add_help=False)
        parser.add_argument("--client", required=True)
        parser.add_argument("--time", type=int, default=1)

        try:
            parsed = parser.parse_args(shlex.split(arg))
        except SystemExit:
            print("Usage: send --client <ip> [--time <seconds>]")
            return

        if parsed.time < 1:
            print("Time must be >= 1")
            return

        try:
            self.manager.send_data(parsed.client, message="data")
            print(f"Data sent successfully to {parsed.client}.")
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to send data: {exc}")

    def do_transfer(self, arg: str) -> None:
        parser = argparse.ArgumentParser(prog="transfer", add_help=False)
        parser.add_argument("--client", required=True)

        try:
            parsed = parser.parse_args(shlex.split(arg))
        except SystemExit:
            print("Usage: transfer --client <ip>")
            return

        bytes_written = self.manager.transfer_buffered_data(parsed.client)
        if bytes_written == 0:
            print(f"No buffered data for client: {parsed.client}")
            return

        print(f"Buffered transfer complete for {parsed.client}. Wrote {bytes_written} bytes.")

    def do_status(self, arg: str) -> None:
        _ = arg
        snapshot = self.manager.status_snapshot()
        print(f"Running: {snapshot['running']}")
        print(f"Ports: {snapshot['ports']}")
        print(f"Tracked clients: {snapshot['total_clients']}")
        print(f"Connected clients: {snapshot['connected_clients']}")
        print("Processing time (seconds):")
        for client_ip, total_time in snapshot["processing_time"].items():
            print(f"  {client_ip}: {total_time:.6f}")

    def do_quit(self, arg: str) -> bool:
        _ = arg
        if self.manager.is_running():
            self.manager.stop()
        print("Bye.")
        return True

    def do_EOF(self, arg: str) -> bool:  # noqa: N802
        print()
        return self.do_quit(arg)


def _configure_logging(level: str) -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, format="[%(levelname)s] %(message)s")


def main() -> int:
    parser = _command_parser()
    args = parser.parse_args()

    _configure_logging(args.log_level)

    manager = ServerManager(
        ports=args.ports,
        output_dir=Path(args.output_dir),
        auto_write=not args.manual_transfer_only,
    )
    shell = ServerShell(manager=manager, default_ports=args.ports)

    def _signal_handler(signum: int, frame: object) -> None:  # noqa: ARG001
        print("\nSignal received, shutting down...")
        if manager.is_running():
            manager.stop()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, _signal_handler)

    shell.cmdloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
