"""Navia's layered clip sounds, made from vanilla events only.

One module per clip, tools/player_motion/navia_audio/<clip>.py, so each clip author owns one file.
A module defines either

    def timeline(clip: dict) -> list[dict]      # clip = the clip's JSON object (length, hit_ticks, ...)

or a constant ``LAYERS = [...]``. Each layer is the same entry audio_arle.py's timelines return:

    {"tick": int, "event": "entity.player.attack.sweep", "volume": 0.6, "pitch": 1.1, "layer": "short label"}

tick 0..clip length (authored ticks: the animation clock, so attack speed scales them), volume 0 < v <= 1,
pitch 0.5..2, event a vanilla sound event id without the "minecraft:" prefix. No resource-pack sounds.

Ownership (do not double these in a clip module):
- gameplay keeps the aim-start click (char/navia/aim_start: crossbow loading start + chain place), the skill shot
  blast (char/navia/fire: firework blast, explode, amethyst break), the burst blast (char/navia/burst), the support
  shells (char/navia/shell_fx), the dash whoosh (player/dash_go), the charge/deny/shard cues and the
  confirmed-hit thud (combat/confirmed_hit_sound, real damage only);
- the clips own everything the body and the props do: swings, drags, kicks, steps, the thrown halberd's spin, the
  parasol (appear, twirl, open, close, dissolve), the burst wind-up and the halberd re-forming on the back.
  The generic normal-attack swing/hit layers and the old fx-frame sounds are switched off for Navia.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent / "navia_audio"
KEYS = ("tick", "event", "volume", "pitch", "layer")


def _load(name: str):
    path = HERE / f"{name}.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"navia_audio_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def timeline(name: str, clip: dict) -> list[dict] | None:
    """Layers of navia_audio/<name>.py; None when the clip has no module (no audio file, no hook)."""
    module = _load(name)
    if module is None:
        return None
    if hasattr(module, "timeline"):
        layers = module.timeline(clip)
    else:
        layers = getattr(module, "LAYERS", [])
    out = []
    for layer in layers or []:
        missing = [k for k in KEYS if k not in layer]
        if missing:
            raise ValueError(f"navia_audio/{name}.py: layer {layer} lacks {missing}")
        out.append({
            "tick": int(layer["tick"]),
            "event": str(layer["event"]).removeprefix("minecraft:"),
            "volume": round(float(layer["volume"]), 3),
            "pitch": round(float(layer["pitch"]), 3),
            "layer": str(layer["layer"]),
        })
    return sorted(out, key=lambda layer: layer["tick"])
