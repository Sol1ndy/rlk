"""Navia skill_fire sound layers (owner: skill). Vanilla sound events only; see player_motion/audio_navia.py.

Timeline from the v4 release (understand/v4.md section 7, fire+ ticks = clip ticks, recovery compressed): a faint
trigger tick (S4), the canopy snapping open, the crystal shard crunches after the blast (S6), the knocked-down
squat, the rise, the canopy rim on the floor (S13), the close, the dissolve shimmer (S14) and the halberd settling
on the back. The blast itself (firework blast, explode, amethyst break) is char/navia/fire at tick 3.
"""


def timeline(clip: dict) -> list[dict]:
    blast = clip.get("activation_tick", 3)
    return [
        {"tick": 0, "event": "block.lever.click", "volume": 0.25, "pitch": 1.9, "layer": "trigger tick (S4)"},
        {"tick": 1, "event": "item.armor.equip_leather", "volume": 0.4, "pitch": 1.6, "layer": "canopy pops open"},
        {"tick": 1, "event": "item.crossbow.loading_middle", "volume": 0.25, "pitch": 1.7, "layer": "canopy mechanism"},
        {"tick": blast + 2, "event": "block.amethyst_block.hit", "volume": 0.4, "pitch": 1.3, "layer": "crystal shard crunch (S6)"},
        {"tick": blast + 2, "event": "block.glass.break", "volume": 0.2, "pitch": 1.7, "layer": "shard glint (S6)"},
        {"tick": blast + 3, "event": "item.armor.equip_leather", "volume": 0.3, "pitch": 0.9, "layer": "knocked back, coat swish"},
        {"tick": blast + 4, "event": "block.amethyst_block.hit", "volume": 0.35, "pitch": 1.5, "layer": "crystal shard crunch (S6)"},
        {"tick": blast + 5, "event": "block.wool.place", "volume": 0.3, "pitch": 0.8, "layer": "squat lands"},
        {"tick": blast + 6, "event": "block.amethyst_cluster.break", "volume": 0.3, "pitch": 1.2, "layer": "shard crackle (S6)"},
        {"tick": 12, "event": "item.armor.equip_leather", "volume": 0.25, "pitch": 1.2, "layer": "rise"},
        {"tick": 14, "event": "block.wool.place", "volume": 0.25, "pitch": 0.8, "layer": "canopy rim on the floor (S13)"},
        {"tick": 15, "event": "item.crossbow.loading_end", "volume": 0.3, "pitch": 1.7, "layer": "canopy closes"},
        {"tick": 15, "event": "item.armor.equip_leather", "volume": 0.22, "pitch": 1.6, "layer": "close rustle"},
        {"tick": 17, "event": "block.amethyst_block.chime", "volume": 0.35, "pitch": 1.9, "layer": "dissolve shimmer (S14)"},
        {"tick": 18, "event": "block.beacon.deactivate", "volume": 0.15, "pitch": 2.0, "layer": "dissolve ring-out (S14)"},
        {"tick": 21, "event": "item.armor.equip_iron", "volume": 0.25, "pitch": 1.4, "layer": "halberd re-forms on the back"},
    ]
