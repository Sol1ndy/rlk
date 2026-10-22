"""Navia skill_aim sound layers (owner: skill). Vanilla sound events only; see player_motion/audio_navia.py.

The aim hold is silent in v4 (only the voice line, which is never reproduced), and a loop must not repeat
sounds (README sound rules), so this clip has no layers.
"""


def timeline(clip: dict) -> list[dict]:
    return []
