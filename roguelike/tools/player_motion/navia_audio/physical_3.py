"""Navia physical_3 sound layers (owner: na3). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

Timeline after v2 A3-A6 (2.27-3.30 s) and v2 section 7, in authored ticks (1.0x, so attack speed scales them):
the halberd swung back (1), the tip-scrape click and drag (2-3), the whip up and out (4-5), the swing down (6), the
planted thunk (7), the release and knee chamber rustle (8), the kick crack as the halberd leaves the foot (10), the
thrown halberd's whirr (11-16) with a light chunk on each of the three hits (13/15/17; the confirmed-hit thud is
gameplay and plays only on real damage), the gold dissolve (18) and the halberd re-forming on her back (21-23).
One chime only, no loops.
Events: all in scratchpad/navia/dp_sound_events.txt except block.stone.hit and block.grindstone.use (standard
vanilla ids).
"""


def timeline(clip: dict) -> list[dict]:
    hits = list(clip.get("hit_ticks") or [13, 15, 17])
    kick = 10
    layers = [
        {"tick": 1, "event": "entity.player.attack.sweep", "volume": 0.18, "pitch": 0.55, "layer": "halberd swung back"},
        {"tick": 2, "event": "block.stone.hit", "volume": 0.3, "pitch": 1.35, "layer": "tip-scrape click"},
        {"tick": 2, "event": "item.trident.hit_ground", "volume": 0.14, "pitch": 1.5, "layer": "metal tip on stone"},
        {"tick": 2, "event": "block.stone.step", "volume": 0.18, "pitch": 0.85, "layer": "sliding lunge step"},
        {"tick": 3, "event": "block.grindstone.use", "volume": 0.07, "pitch": 1.7, "layer": "drag scrape"},
        {"tick": 4, "event": "entity.player.attack.sweep", "volume": 0.22, "pitch": 0.75, "layer": "whip up"},
        {"tick": 6, "event": "entity.player.attack.sweep", "volume": 0.2, "pitch": 0.6, "layer": "swing down"},
        {"tick": 7, "event": "block.heavy_core.hit", "volume": 0.3, "pitch": 1.1, "layer": "planted thunk"},
        {"tick": 7, "event": "item.trident.hit_ground", "volume": 0.24, "pitch": 0.8, "layer": "spear point bites"},
        {"tick": 8, "event": "item.armor.equip_leather", "volume": 0.14, "pitch": 1.2, "layer": "knee chamber rustle"},
        {"tick": kick, "event": "entity.player.attack.knockback", "volume": 0.45, "pitch": 1.2, "layer": "kick crack"},
        {"tick": kick, "event": "item.trident.throw", "volume": 0.38, "pitch": 0.8, "layer": "halberd launched"},
        {"tick": kick, "event": "entity.player.attack.strong", "volume": 0.16, "pitch": 1.4, "layer": "kick snap"},
        {"tick": kick + 1, "event": "item.trident.riptide_1", "volume": 0.16, "pitch": 1.5, "layer": "spin-up whirr"},
    ]
    for i, t in enumerate((12, 14, 16)):
        layers.append({"tick": t, "event": "entity.player.attack.sweep", "volume": 0.15, "pitch": 1.0 + 0.12 * i,
                       "layer": "whirr"})
    for i, t in enumerate(hits):
        layers.append({"tick": t, "event": "item.spear.attack", "volume": 0.12, "pitch": 1.2 + 0.1 * i,
                       "layer": "halberd chunk"})
    layers += [
        {"tick": 18, "event": "entity.illusioner.mirror_move", "volume": 0.16, "pitch": 1.6, "layer": "gold dissolve"},
        {"tick": 21, "event": "block.amethyst_block.chime", "volume": 0.2, "pitch": 1.5, "layer": "re-form chime"},
        {"tick": 23, "event": "item.armor.equip_iron", "volume": 0.16, "pitch": 1.15, "layer": "settles on the back"},
    ]
    length = int(clip.get("length", 24))
    return [layer for layer in layers if 0 <= layer["tick"] <= length]
