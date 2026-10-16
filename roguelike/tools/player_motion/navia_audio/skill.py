"""Navia skill (tap) sound layers (owner: skill). Vanilla sound events only; see player_motion/audio_navia.py.

Timeline from the v5 tap (understand/v5.md section 7, rel ticks = clip ticks up to the shot at 7, the recovery
compressed): a soft shimmer as the parasol appears, a light swish on the twirl, the canopy snapping open with its
mechanism whirring (A1), the recoil slide and the knee landing, the Geo crackle of the shrapnel and petals (A3),
the rise, the canopy rim on the floor, the fold click (A10), the dissolve whoof and shimmer (A11-A12) and the
halberd settling on the back. The shot itself (firework blast, explode, amethyst break) is char/navia/fire.
"""


def timeline(clip: dict) -> list[dict]:
    shot = clip.get("activation_tick", 7)
    return [
        {"tick": 1, "event": "block.amethyst_block.chime", "volume": 0.25, "pitch": 1.8, "layer": "parasol appears"},
        {"tick": 2, "event": "entity.player.attack.sweep", "volume": 0.2, "pitch": 1.7, "layer": "twirl swish"},
        {"tick": 5, "event": "item.armor.equip_leather", "volume": 0.55, "pitch": 1.6, "layer": "canopy snaps open (A1 cloth)"},
        {"tick": 5, "event": "item.crossbow.loading_middle", "volume": 0.35, "pitch": 1.6, "layer": "canopy mechanism whir (A1)"},
        {"tick": 5, "event": "block.amethyst_block.chime", "volume": 0.3, "pitch": 1.6, "layer": "flare glitter (A1)"},
        {"tick": shot + 2, "event": "item.armor.equip_leather", "volume": 0.3, "pitch": 0.9, "layer": "recoil, coat swish"},
        {"tick": shot + 4, "event": "entity.breeze.slide", "volume": 0.25, "pitch": 1.3, "layer": "recoil slide"},
        {"tick": shot + 6, "event": "block.amethyst_cluster.break", "volume": 0.5, "pitch": 1.3, "layer": "Geo shrapnel crackle (A3)"},
        {"tick": shot + 6, "event": "entity.firework_rocket.twinkle", "volume": 0.25, "pitch": 1.4, "layer": "petal sparkle (A3)"},
        {"tick": shot + 7, "event": "block.wool.place", "volume": 0.3, "pitch": 0.8, "layer": "knee lands"},
        {"tick": 20, "event": "item.armor.equip_leather", "volume": 0.25, "pitch": 1.2, "layer": "rise (A9)"},
        {"tick": 23, "event": "block.wool.place", "volume": 0.2, "pitch": 0.9, "layer": "canopy rim on the floor"},
        {"tick": 24, "event": "item.crossbow.loading_end", "volume": 0.35, "pitch": 1.7, "layer": "canopy folds (A10)"},
        {"tick": 24, "event": "item.armor.equip_leather", "volume": 0.25, "pitch": 1.6, "layer": "fold rustle (A10)"},
        {"tick": 27, "event": "entity.illusioner.mirror_move", "volume": 0.25, "pitch": 1.5, "layer": "parasol dissolves (A11)"},
        {"tick": 28, "event": "block.amethyst_block.chime", "volume": 0.4, "pitch": 1.9, "layer": "dissolve shimmer (A12)"},
        {"tick": 28, "event": "entity.firework_rocket.twinkle", "volume": 0.18, "pitch": 1.8, "layer": "dissolve sparkle (A12)"},
        {"tick": 31, "event": "item.armor.equip_iron", "volume": 0.25, "pitch": 1.4, "layer": "halberd re-forms on the back"},
    ]
