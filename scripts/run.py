#!/usr/bin/env python3
"""Convenience entrypoints with PYTHONPATH=repo root."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "align"
    sys.argv = [target, *sys.argv[2:]]
    if target == "align":
        runpy.run_module("pipeline.align", run_name="__main__")
    elif target == "translate":
        runpy.run_module("translate.engine", run_name="__main__")
    else:
        raise SystemExit(f"Unknown command: {target} (use align|translate)")
