"""Navia burst sound layers (owner: burst). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

Timeline from the reference audio (v1 §7.3, v6 §7.3; v1/v6 rel tick ~ clip tick - 1 during the flourish):
the parasol appears almost silently, the swing up is the loud snap/swish with a glitter chime, a low riser
follows, the cannon is cocked with a double clack at ~22-23, distant volley reports and a swell lead into a
short lull (the radial zoom), and the blast lands at 34. The blast itself (explode + large blast), the support
shells and their impacts are gameplay sounds (char/navia/burst, char/navia/shell_fx) and are not repeated here.
After the blast: a low cannon-report thump, the air hiss and the cosmetic initial-barrage pops (the clip fx
draw those shells), then the put-away (swing, fold, cane tap, dissolve) and a quiet re-form on the back.

Retimed (D11): the ticks below are the original layers pushed through the clip time-warp (playback 100,
Genshin cadence and recovery). This literal list is the source now; edit it directly."""

LAYERS = [
    {"tick": 1, "event": "block.amethyst_block.resonate", "volume": 0.12, "pitch": 1.6, "layer": "parasol materialise shimmer"},
    {"tick": 6, "event": "entity.ender_dragon.flap", "volume": 0.3, "pitch": 1.8, "layer": "canopy snap"},
    {"tick": 6, "event": "entity.player.attack.sweep", "volume": 0.32, "pitch": 1.25, "layer": "flourish swish"},
    {"tick": 7, "event": "entity.firework_rocket.twinkle", "volume": 0.22, "pitch": 1.3, "layer": "geo glitter"},
    {"tick": 7, "event": "block.amethyst_block.chime", "volume": 0.4, "pitch": 1.1, "layer": "swing-up chime"},
    {"tick": 11, "event": "item.armor.equip_leather", "volume": 0.2, "pitch": 1.2, "layer": "parasol on the shoulder"},
    {"tick": 11, "event": "block.amethyst_block.chime", "volume": 0.22, "pitch": 1.35, "layer": "settle chime"},
    {"tick": 14, "event": "block.respawn_anchor.charge", "volume": 0.3, "pitch": 0.8, "layer": "low riser"},
    {"tick": 22, "event": "item.crossbow.loading_end", "volume": 0.45, "pitch": 0.75, "layer": "cannon cock 1"},
    {"tick": 23, "event": "block.iron_door.close", "volume": 0.3, "pitch": 1.3, "layer": "cannon cock 2"},
    {"tick": 24, "event": "entity.breeze.charge", "volume": 0.25, "pitch": 0.6, "layer": "pre-blast rumble swell"},
    {"tick": 25, "event": "entity.firework_rocket.large_blast_far", "volume": 0.3, "pitch": 0.6, "layer": "distant volley 1"},
    {"tick": 29, "event": "entity.firework_rocket.large_blast_far", "volume": 0.25, "pitch": 0.55, "layer": "distant volley 2"},
    {"tick": 30, "event": "entity.breeze.inhale", "volume": 0.28, "pitch": 0.8, "layer": "suck-in"},
    {"tick": 36, "event": "item.mace.smash_ground_heavy", "volume": 0.3, "pitch": 0.7, "layer": "cannon report thump"},
    {"tick": 38, "event": "block.fire.extinguish", "volume": 0.2, "pitch": 1.5, "layer": "shell air hiss"},
    {"tick": 39, "event": "entity.firework_rocket.blast", "volume": 0.28, "pitch": 0.9, "layer": "barrage pop 1"},
    {"tick": 39, "event": "entity.generic.explode", "volume": 0.14, "pitch": 1.35, "layer": "barrage pop 1 body"},
    {"tick": 41, "event": "entity.firework_rocket.blast", "volume": 0.26, "pitch": 1.05, "layer": "barrage pop 2"},
    {"tick": 43, "event": "entity.firework_rocket.blast", "volume": 0.24, "pitch": 0.85, "layer": "barrage pop 3"},
    {"tick": 43, "event": "entity.generic.explode", "volume": 0.12, "pitch": 1.4, "layer": "barrage pop 3 body"},
    {"tick": 45, "event": "entity.firework_rocket.blast", "volume": 0.22, "pitch": 1.0, "layer": "barrage pop 4"},
    {"tick": 47, "event": "entity.firework_rocket.blast", "volume": 0.18, "pitch": 0.95, "layer": "barrage pop 5"},
    {"tick": 86, "event": "entity.player.attack.sweep", "volume": 0.18, "pitch": 1.7, "layer": "parasol off the shoulder"},
    {"tick": 92, "event": "item.armor.equip_leather", "volume": 0.28, "pitch": 1.3, "layer": "parasol folds"},
    {"tick": 94, "event": "block.chain.hit", "volume": 0.2, "pitch": 1.7, "layer": "ferrule tap"},
    {"tick": 96, "event": "entity.firework_rocket.twinkle", "volume": 0.15, "pitch": 1.5, "layer": "dissolve glitter"},
    {"tick": 98, "event": "block.amethyst_block.chime", "volume": 0.2, "pitch": 1.8, "layer": "dissolve chime"},
    {"tick": 101, "event": "block.amethyst_block.resonate", "volume": 0.14, "pitch": 1.25, "layer": "re-form shimmer"},
    {"tick": 105, "event": "item.armor.equip_iron", "volume": 0.16, "pitch": 1.4, "layer": "halberd settles on the back"},
]


def timeline(clip: dict) -> list[dict]:
    length = int(clip.get("length", 108))
    return [dict(layer) for layer in LAYERS if 0 <= layer["tick"] <= length]
