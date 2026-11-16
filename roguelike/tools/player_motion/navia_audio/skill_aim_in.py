"""Navia skill_aim_in sound layers (owner: skill). Vanilla sound events only; see player_motion/audio_navia.py.

Timeline from the v4 hold (understand/v4.md section 7, rel ticks = clip ticks): the parasol materialises with a
metallic shimmer and a frill rattle (S1), a low swish through the first spin, the swing-up whoosh (S2), the
overhead spin with a soft swell as the aim engages (S3) and a light settle into the stance. The aim-start click
(crossbow loading start + chain place) is gameplay (char/navia/aim_start), so it is not repeated here.
"""


def timeline(clip: dict) -> list[dict]:
    return [
        {"tick": 2, "event": "block.stone.step", "volume": 0.2, "pitch": 1.1, "layer": "pivot step"},
        {"tick": 4, "event": "block.amethyst_block.chime", "volume": 0.45, "pitch": 1.6, "layer": "parasol materialises (S1)"},
        {"tick": 4, "event": "item.armor.equip_leather", "volume": 0.35, "pitch": 1.5, "layer": "frill rattle (S1)"},
        {"tick": 6, "event": "entity.player.attack.sweep", "volume": 0.25, "pitch": 1.3, "layer": "low ferrule sweep"},
        {"tick": 9, "event": "entity.player.attack.sweep", "volume": 0.5, "pitch": 0.8, "layer": "swing-up whoosh (S2)"},
        {"tick": 9, "event": "item.trident.throw", "volume": 0.3, "pitch": 1.4, "layer": "swing-up air (S2)"},
        {"tick": 12, "event": "entity.player.attack.sweep", "volume": 0.3, "pitch": 1.2, "layer": "overhead spin (S3)"},
        {"tick": 12, "event": "block.respawn_anchor.charge", "volume": 0.22, "pitch": 1.7, "layer": "aim engages, low swell (S3)"},
        {"tick": 15, "event": "item.armor.equip_leather", "volume": 0.25, "pitch": 0.9, "layer": "drop into the stance"},
    ]
