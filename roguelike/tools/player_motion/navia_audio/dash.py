"""Navia dash sound layers (owner: dash_sheathe). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

v7 §8: every character's dash plays the same soft whoosh, which gameplay already owns (player/dash_go:
wind_charge burst + breeze slide on the dash tick), so this clip adds none. Navia's own dash has no extra
sound in the reference; her gold visuals borrow the timbre of her swap-in shimmer, very quietly:
- a soft amethyst chime when the gold rose appears behind her hips (t2, v7 §8 suggestion);
- a faint coat flutter as the body whips into the lean (t1).
Both names are already used in the pack (scratchpad/navia/dp_sound_events.txt).
"""


def timeline(clip: dict) -> list[dict]:
    return [
        {"tick": 1, "event": "item.armor.equip_leather", "volume": 0.16, "pitch": 1.35, "layer": "coat flutter"},
        {"tick": 2, "event": "block.amethyst_block.chime", "volume": 0.22, "pitch": 1.8, "layer": "gold rose shimmer"},
    ]
