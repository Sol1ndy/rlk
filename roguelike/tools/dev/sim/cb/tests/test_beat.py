#!/usr/bin/env python3
"""test_beat.py: the perfect parry / perfect dodge beat (round V, lane VP) - the runner of test_cb.py's sections `beat` and
`beatloop` (the harness lives there; run from a copy outside the datapack, tools/dev/sim/README.md 1).

    python3 test_beat.py <datapack root>
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.exit(subprocess.run([sys.executable, str(HERE / 'test_cb.py'), sys.argv[1], 'beat', 'beatloop']).returncode)
