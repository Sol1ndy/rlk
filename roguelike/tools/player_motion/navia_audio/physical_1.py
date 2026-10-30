"""Navia physical_1 sound layers (owner: na12). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

Timeline from v2 A1 / v3 §7.5 (NA1), offsets from the contact tick (hit = 9, authored ticks):
- the wind-up is almost silent in the video: a soft cloth/grip rustle only;
- a heavy, low claymore whoosh just before contact, with a little air weight behind it;
- the bright metal "shing" of the edge right after contact (the body thud is the confirmed-hit sound);
- the halberd head drops onto the floor at hit+4: a weighty thud with a short low tail.
All names are already used in the pack (scratchpad/navia/dp_sound_events.txt).

Retimed (D11): the ticks below are the original layers pushed through the clip time-warp (playback 100,
Genshin cadence and recovery). This literal list is the source now; edit it directly."""

LAYERS = [
    {"tick": 2, "event": "item.armor.equip_leather", "volume": 0.18, "pitch": 1.1, "layer": "wind-up grip"},
    {"tick": 7, "event": "entity.player.attack.sweep", "volume": 0.5, "pitch": 0.62, "layer": "heavy whoosh"},
    {"tick": 8, "event": "item.trident.throw", "volume": 0.22, "pitch": 0.62, "layer": "swing weight"},
    {"tick": 10, "event": "item.spear.attack", "volume": 0.22, "pitch": 0.85, "layer": "edge shing"},
    {"tick": 15, "event": "item.mace.smash_ground", "volume": 0.38, "pitch": 0.9, "layer": "head thud"},
    {"tick": 15, "event": "block.heavy_core.hit", "volume": 0.2, "pitch": 0.65, "layer": "thud body"},
]


def timeline(clip: dict) -> list[dict]:
    length = int(clip.get("length", 55))
    return [dict(layer) for layer in LAYERS if 0 <= layer["tick"] <= length]
