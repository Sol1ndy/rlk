"""Navia dash sound layers (owner: dash_sheathe). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

Return one dict per layer: {"tick": int, "event": "entity.player.attack.sweep", "volume": 0.6, "pitch": 1.1,
"layer": "label"}. Ticks are authored clip ticks (0..length), so they follow attack speed like the animation.
"""


def timeline(clip: dict) -> list[dict]:
    return []
