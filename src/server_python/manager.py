from __future__ import annotations

import logging
import socket
import socketserver
import threading
import time
from pathlib import Path

from .models import ClientRecord
from .protocol import decode_complete_uint32_words, strip_termination_words
from .storage import append_client_words


class _ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class _ClientHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        manager: ServerManager = self.server.manager  # type: ignore[attr-defined]
        client_ip = self.client_address[0]
        client_port = self.server.server_address[1]

        manager.register_client(client_ip=client_ip, port=client_port, sock=self.request)

        try:
            while True:
                packet = self.request.recv(65536)
                if not packet:
                    break
                manager.handle_client_data(client_ip=client_ip, packet=packet)
        except (ConnectionResetError, OSError):
            pass
        finally:
            manager.unregister_client(client_ip=client_ip, sock=self.request)


class ServerManager:
    def __init__(self, ports: list[int], output_dir: Path, auto_write: bool = True) -> None:
        self.default_ports = ports
        self.output_dir = output_dir
        self.auto_write = auto_write

        self._servers: dict[int, _ThreadedTCPServer] = {}
        self._threads: dict[int, threading.Thread] = {}
        self._clients: dict[str, ClientRecord] = {}
        self._client_sockets: dict[str, socket.socket] = {}
        self._buffers: dict[str, list[int]] = {}
        self._lock = threading.RLock()

    def is_running(self) -> bool:
        with self._lock:
            return bool(self._servers)

    def running_ports(self) -> list[int]:
        with self._lock:
            return sorted(self._servers.keys())

    def start(self, ports: list[int] | None = None) -> list[int]:
        target_ports = ports if ports else self.default_ports
        started_ports: list[int] = []

        with self._lock:
            if self._servers:
                return []

            for port in target_ports:
                server = _ThreadedTCPServer(("0.0.0.0", port), _ClientHandler)
                server.manager = self  # type: ignore[attr-defined]
                thread = threading.Thread(target=server.serve_forever, daemon=True)

                self._servers[port] = server
                self._threads[port] = thread
                thread.start()
                started_ports.append(port)

                logging.info("Server started on port %s", port)

        return started_ports

    def stop(self) -> None:
        with self._lock:
            server_items = list(self._servers.items())
            thread_items = list(self._threads.items())

            self._servers = {}
            self._threads = {}
            self._clients = {}
            self._client_sockets = {}
            self._buffers = {}

        for _, server in server_items:
            server.shutdown()
            server.server_close()

        for _, thread in thread_items:
            thread.join(timeout=1.0)

        logging.info("All servers stopped.")

    def register_client(self, client_ip: str, port: int, sock: socket.socket) -> None:
        with self._lock:
            if client_ip in self._clients:
                logging.warning(
                    "Client IP collision for %s. Latest connection overrides previous mapping.",
                    client_ip,
                )

            self._clients[client_ip] = ClientRecord(ip=client_ip, port=port)
            self._client_sockets[client_ip] = sock
            self._buffers.setdefault(client_ip, [])

        logging.info("New client connected to port %s: %s", port, client_ip)

    def unregister_client(self, client_ip: str, sock: socket.socket) -> None:
        with self._lock:
            mapped_sock = self._client_sockets.get(client_ip)
            if mapped_sock is not sock:
                return

            if client_ip in self._clients:
                self._clients[client_ip].status = "Disconnected"
            self._client_sockets.pop(client_ip, None)

        logging.info("Client disconnected: %s", client_ip)

    def handle_client_data(self, client_ip: str, packet: bytes) -> None:
        start_time = time.perf_counter()

        words, discarded = decode_complete_uint32_words(packet)
        payload, had_termination = strip_termination_words(words)

        if payload:
            if self.auto_write:
                bytes_written = append_client_words(client_ip, payload, self.output_dir)
                logging.info(
                    "Written %s bytes of uint32 data to file for client %s.",
                    bytes_written,
                    client_ip,
                )
            else:
                with self._lock:
                    self._buffers.setdefault(client_ip, []).extend(payload)

        if discarded:
            logging.info("Discarded %s leftover bytes from client %s.", discarded, client_ip)

        if had_termination:
            logging.info("End of transmission signal received from client: %s", client_ip)

        elapsed = time.perf_counter() - start_time
        with self._lock:
            if client_ip in self._clients:
                self._clients[client_ip].total_processing_time += elapsed

    def list_clients(self) -> list[tuple[str, int, str]]:
        with self._lock:
            rows = [
                (record.ip, record.port, record.status)
                for record in self._clients.values()
            ]
        rows.sort(key=lambda item: item[0])
        return rows

    def send_data(self, client_ip: str, message: str = "data") -> None:
        with self._lock:
            sock = self._client_sockets.get(client_ip)

        if sock is None:
            raise ValueError("Selected client is not currently connected.")

        sock.sendall(message.encode("utf-8"))

    def transfer_buffered_data(self, client_ip: str) -> int:
        with self._lock:
            buffered = list(self._buffers.get(client_ip, []))
            self._buffers[client_ip] = []

        if not buffered:
            return 0

        return append_client_words(client_ip, buffered, self.output_dir)

    def status_snapshot(self) -> dict[str, object]:
        with self._lock:
            total_clients = len(self._clients)
            connected_clients = len(self._client_sockets)
            processing_time = {
                ip: record.total_processing_time for ip, record in self._clients.items()
            }

        return {
            "running": self.is_running(),
            "ports": self.running_ports(),
            "total_clients": total_clients,
            "connected_clients": connected_clients,
            "processing_time": processing_time,
        }
