"""Navia sheathe sound layers (owner: dash_sheathe). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

v10 §8.1 (PA1, identical in PA2): the put-away is very quiet and has no voice. Ticks follow the clip beats
(shoulder 8, wheel bottom 20, top 26, regrip 30, plant 36, glow-up 40, dissolve 42, back speck 48, growth 53).
All names are already used in the pack (scratchpad/navia/dp_sound_events.txt).
"""


def timeline(clip: dict) -> list[dict]:
    return [
        {"tick": 4, "event": "entity.breeze.slide", "volume": 0.08, "pitch": 1.5, "layer": "tip leaves the floor"},
        {"tick": 7, "event": "entity.player.attack.sweep", "volume": 0.2, "pitch": 0.7, "layer": "onto the shoulder"},
        {"tick": 19, "event": "entity.player.attack.sweep", "volume": 0.26, "pitch": 0.55, "layer": "wheel bottom whoosh"},
        {"tick": 19, "event": "item.trident.throw", "volume": 0.12, "pitch": 0.6, "layer": "wheel weight"},
        {"tick": 25, "event": "entity.breeze.slide", "volume": 0.12, "pitch": 1.2, "layer": "wheel top air"},
        {"tick": 30, "event": "item.armor.equip_iron", "volume": 0.22, "pitch": 0.8, "layer": "regrip"},
        {"tick": 36, "event": "item.trident.hit_ground", "volume": 0.4, "pitch": 0.8, "layer": "plant clank"},
        {"tick": 37, "event": "block.chain.place", "volume": 0.28, "pitch": 0.7, "layer": "plant ring"},
        {"tick": 40, "event": "block.amethyst_block.chime", "volume": 0.25, "pitch": 1.6, "layer": "glow-up"},
        {"tick": 42, "event": "entity.firework_rocket.twinkle", "volume": 0.08, "pitch": 1.6, "layer": "dissolve sparkle"},
        {"tick": 48, "event": "block.amethyst_block.resonate", "volume": 0.14, "pitch": 1.3, "layer": "back speck"},
        {"tick": 53, "event": "block.enchantment_table.use", "volume": 0.1, "pitch": 1.6, "layer": "back silhouette shimmer"},
    ]
