"""Navia skill_fire sound layers (owner: skill). Vanilla sound events only; see player_motion/audio_navia.py.

Timeline from the v4 release (understand/v4.md section 7, fire+ ticks = clip ticks, recovery compressed): a faint
trigger tick (S4) into a near-silent beat (the canopy pop is silent in the video; only the optional soft cloth snap
v4 proposes), the crystal shard crunches after the blast (S6), the knocked-down squat, the rise, the canopy rim on
the floor (S13), the silent close, the dissolve shimmer (S14) and the halberd settling on the back. The blast itself
(firework blast, explode, amethyst break) is char/navia/fire at tick 3.

Retimed (D11): the ticks below are the original layers pushed through the clip time-warp (playback 100,
Genshin cadence and recovery). This literal list is the source now; edit it directly."""

LAYERS = [
    {"tick": 0, "event": "block.lever.click", "volume": 0.25, "pitch": 1.9, "layer": "trigger tick (S4)"},
    {"tick": 1, "event": "item.armor.equip_leather", "volume": 0.2, "pitch": 1.5, "layer": "canopy pops open (soft cloth snap; v4: silent)"},
    {"tick": 5, "event": "block.amethyst_block.hit", "volume": 0.4, "pitch": 1.3, "layer": "crystal shard crunch (S6)"},
    {"tick": 5, "event": "block.glass.break", "volume": 0.2, "pitch": 1.7, "layer": "shard glint (S6)"},
    {"tick": 7, "event": "item.armor.equip_leather", "volume": 0.3, "pitch": 0.9, "layer": "knocked back, coat swish"},
    {"tick": 15, "event": "block.amethyst_block.hit", "volume": 0.35, "pitch": 1.5, "layer": "crystal shard crunch (S6)"},
    {"tick": 22, "event": "block.wool.place", "volume": 0.3, "pitch": 0.8, "layer": "squat lands"},
    {"tick": 30, "event": "block.amethyst_cluster.break", "volume": 0.3, "pitch": 1.2, "layer": "shard crackle (S6)"},
    {"tick": 49, "event": "item.armor.equip_leather", "volume": 0.25, "pitch": 1.2, "layer": "rise"},
    {"tick": 51, "event": "block.wool.place", "volume": 0.25, "pitch": 0.8, "layer": "canopy rim on the floor (S13)"},
    {"tick": 57, "event": "item.armor.equip_leather", "volume": 0.1, "pitch": 1.6, "layer": "close rustle (very quiet; v4: silent close)"},
    {"tick": 62, "event": "block.amethyst_block.chime", "volume": 0.35, "pitch": 1.9, "layer": "dissolve shimmer (S14)"},
    {"tick": 64, "event": "block.beacon.deactivate", "volume": 0.15, "pitch": 2.0, "layer": "dissolve ring-out (S14)"},
    {"tick": 67, "event": "item.armor.equip_iron", "volume": 0.25, "pitch": 1.4, "layer": "halberd re-forms on the back"},
]


def timeline(clip: dict) -> list[dict]:
    length = int(clip.get("length", 70))
    return [dict(layer) for layer in LAYERS if 0 <= layer["tick"] <= length]
