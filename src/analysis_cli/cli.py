from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ANALYSIS_SCRIPTS = {
    "frequency": "frequencyAnalysis.py",
    "sync": "synchronizationAnalysis.py",
    "all-frequency": "AllFrequencyAnalysis.py",
    "cross-correlation": "crossCorrelate.py",
    "statistical": "statisticalAnalysis.py",
    "scatter": "scatter.py",
    "superimpose": "superImpose.py",
    "superimpose-expt2": "superImpose_expt2.py",
    "time-sync-avg": "timeSyncAvg.py",
    "sine-wave": "sineWave.py",
}


def _resolve_script_path(script_name: str) -> Path | None:
    candidates = [
        Path.cwd() / script_name,
        Path(__file__).resolve().parents[2] / script_name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _run_script(script_name: str, script_args: list[str]) -> int:
    script_path = _resolve_script_path(script_name)
    if script_path is None:
        print(f"Script not found: {Path.cwd() / script_name}")
        return 1

    cmd = [sys.executable, str(script_path), *script_args]
    completed = subprocess.run(cmd, check=False)
    return int(completed.returncode)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="analysis-cli",
        description="Analysis project CLI wrappers",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a known analysis workflow")
    run_parser.add_argument("workflow", choices=sorted(ANALYSIS_SCRIPTS.keys()))
    run_parser.add_argument("workflow_args", nargs="*", help="Arguments passed to the analysis script")

    custom_parser = subparsers.add_parser("run-script", help="Run any analysis script by file name")
    custom_parser.add_argument("script_name", help="Script file name in repo root")
    custom_parser.add_argument("script_args", nargs="*", help="Arguments passed to the script")

    list_parser = subparsers.add_parser("list", help="List available analysis workflows")
    list_parser.set_defaults(command="list")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "run":
        script_name = ANALYSIS_SCRIPTS[args.workflow]
        return _run_script(script_name, args.workflow_args)

    if args.command == "run-script":
        return _run_script(args.script_name, args.script_args)

    if args.command == "list":
        print("Available workflows:")
        for name, script in sorted(ANALYSIS_SCRIPTS.items()):
            print(f"- {name}: {script}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
