# Server_Python

Python CLI migration of the MATLAB server app. The CLI keeps the same core behavior:

- Multiple TCP listeners (default ports: 5001, 5002, 5003, 5004)
- Client tracking keyed by IP (MATLAB parity)
- Incoming data parsed as uint32 words
- Termination marker handling for `0xFFFFFFFF`
- Binary append writes to per-client files

## Requirements

- Python 3.11+

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Run

```powershell
server-cli --ports 5001 5002 5003 5004 --output-dir .
```

## CLI Commands

- `start [--ports 5001 5002 ...]`
- `stop`
- `list`
- `send --client <ip> [--time <seconds>]`
- `transfer --client <ip>`
- `status`
- `quit`

Notes:

- The `send` command always transmits the literal string `data` to mirror MATLAB.
- `--time` is accepted for compatibility but not used in payload construction.
- By default, incoming payload words are written immediately.
- Use `--manual-transfer-only` to buffer incoming data and flush with `transfer`.

## Output Files

Received uint32 payload data is appended to:

- `ClientData_<client-ip>.bin`

IPv6 separators are sanitized (`:` -> `_`) in file names.

## Tests

```powershell
python -m unittest discover -s tests -v
```
