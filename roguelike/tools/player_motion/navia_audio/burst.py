"""Navia burst sound layers (owner: burst). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

Timeline from the reference audio (v1 §7.3, v6 §7.3; v1/v6 rel tick ~ clip tick - 1 during the flourish):
the parasol appears almost silently, the swing up is the loud snap/swish with a glitter chime, a low riser
follows, the cannon is cocked with a double clack at ~22-23, distant volley reports and a swell lead into a
short lull (the radial zoom), and the blast lands at 34. The blast itself (explode + large blast), the support
shells and their impacts are gameplay sounds (char/navia/burst, char/navia/shell_fx) and are not repeated here.
After the blast: a low cannon-report thump, the air hiss and the cosmetic initial-barrage pops (the clip fx
draw those shells), then the put-away (swing, fold, cane tap, dissolve) and a quiet re-form on the back.
"""


def timeline(clip: dict) -> list[dict]:
    blast = int(clip.get("activation_tick", 34))
    layers = [
        # cast: the parasol materialises with a faint shimmer (v1 A0; no sound on the parasol frame in v6)
        (1, "block.amethyst_block.resonate", 0.12, 1.6, "parasol materialise shimmer"),
        # swing up / twirl (v1 A1 rel 4.6, v6 A1 rel 3.3-5.2): canopy snap + swish, then glitter
        (6, "entity.ender_dragon.flap", 0.30, 1.8, "canopy snap"),
        (6, "entity.player.attack.sweep", 0.32, 1.25, "flourish swish"),
        (7, "entity.firework_rocket.twinkle", 0.22, 1.3, "geo glitter"),
        (7, "block.amethyst_block.chime", 0.40, 1.1, "swing-up chime"),
        # settles on the shoulder (v6 A1b rel 10.3)
        (11, "item.armor.equip_leather", 0.20, 1.2, "parasol on the shoulder"),
        (11, "block.amethyst_block.chime", 0.22, 1.35, "settle chime"),
        # low riser (v1 A2 rel 13-16, v6 A1c)
        (14, "block.respawn_anchor.charge", 0.30, 0.8, "low riser"),
        # cannon cocked: clack-clack (v1 A3 rel 22.0 / 23.2, v6 A2 rel 23.0), rumble swell, distant volleys
        (22, "item.crossbow.loading_end", 0.45, 0.75, "cannon cock 1"),
        (23, "block.iron_door.close", 0.30, 1.3, "cannon cock 2"),
        (24, "entity.breeze.charge", 0.25, 0.6, "pre-blast rumble swell"),
        (25, "entity.firework_rocket.large_blast_far", 0.30, 0.6, "distant volley 1"),
        (29, "entity.firework_rocket.large_blast_far", 0.25, 0.55, "distant volley 2"),
        # lull / suck-in during the radial zoom (v6 A2c rel 31-34)
        (30, "entity.breeze.inhale", 0.28, 0.8, "suck-in"),
        # blast + 2..3: cannon report body after gameplay's blast crack (v1 A6, v6 A3b rel 36.6)
        (blast + 2, "item.mace.smash_ground_heavy", 0.30, 0.7, "cannon report thump"),
        # shells whistling in (v1 A7 rel 39.7)
        (blast + 4, "block.fire.extinguish", 0.20, 1.5, "shell air hiss"),
        # cosmetic initial barrage (v1 A8), on the clip fx impact ticks 39/41/43/45/47
        (39, "entity.firework_rocket.blast", 0.28, 0.9, "barrage pop 1"),
        (39, "entity.generic.explode", 0.14, 1.35, "barrage pop 1 body"),
        (41, "entity.firework_rocket.blast", 0.26, 1.05, "barrage pop 2"),
        (43, "entity.firework_rocket.blast", 0.24, 0.85, "barrage pop 3"),
        (43, "entity.generic.explode", 0.12, 1.4, "barrage pop 3 body"),
        (45, "entity.firework_rocket.blast", 0.22, 1.0, "barrage pop 4"),
        (47, "entity.firework_rocket.blast", 0.18, 0.95, "barrage pop 5"),
        # put-away (v6 A7, v1 A11): swing off the shoulder, fold, cane tap, dissolve
        (40, "entity.player.attack.sweep", 0.18, 1.7, "parasol off the shoulder"),
        (43, "item.armor.equip_leather", 0.28, 1.3, "parasol folds"),
        (44, "block.chain.hit", 0.20, 1.7, "ferrule tap"),
        (45, "entity.firework_rocket.twinkle", 0.15, 1.5, "dissolve glitter"),
        (46, "block.amethyst_block.chime", 0.20, 1.8, "dissolve chime"),
        # halberd re-forms on the back (v6 E13 is silent; a soft shimmer and a settle clink)
        (48, "block.amethyst_block.resonate", 0.14, 1.25, "re-form shimmer"),
        (51, "item.armor.equip_iron", 0.16, 1.4, "halberd settles on the back"),
    ]
    return [{"tick": t, "event": e, "volume": v, "pitch": p, "layer": name} for t, e, v, p, name in layers]
