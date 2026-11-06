"""Skirk's authored-frame sound palette, composed only from vanilla events.

Moving blades use sweeps and short air draws. Infusion adds one quiet cold
breath instead of glass, crystalline shattering or a ringing combo tail.
Body impacts belong to confirmed-damage feedback, never normal animation
frames; a missed cut therefore leaves room for the hit sound when it lands.
No recorded Genshin audio is loaded or copied by this module.
"""

from __future__ import annotations


def timeline(name: str, clip: dict) -> list[dict]:
    """Return vanilla layers without modifying animation or gameplay timing."""
    out: list[dict] = []

    def add(tick: int, event: str, volume: float, pitch: float, layer: str) -> None:
        out.append({
            "tick": max(0, int(tick)),
            "event": event,
            "volume": round(volume, 3),
            "pitch": round(pitch, 3),
            "layer": layer,
        })

    if clip.get("loop", False) or not clip.get("audio", True):
        return out

    hits = clip.get("hit_ticks", [])
    if name.startswith(("physical_", "infused_")):
        infused = name.startswith("infused_")
        number = int(name.rsplit("_", 1)[1])
        # N1 crosses the body, N2 cuts back, N3 has two rising cuts, N4
        # thrusts/spins and N5 delivers a deliberately heavier finishing cut.
        sweep_pitch = (0.78, 0.91, 0.88, 0.80, 0.65)[number - 1]
        sweep_volume = (0.48, 0.46, 0.41, 0.49, 0.62)[number - 1]

        # One short breath per attack at most. Even N3's second cut gets no
        # extra cold tail; N5 uses its windup draw as the same single layer.
        if number == 5:
            add(max(0, hits[0] - 5), "entity.breeze.slide",
                0.14 if infused else 0.12, 0.72, "finisher-air-draw")
        elif infused:
            add(max(0, hits[0] - 2), "entity.breeze.slide", 0.085, 0.80,
                "cold-air-draw")

        for index, hit in enumerate(hits):
            # Keep the fast second N3 cut distinct without faking contact.
            pitch_offset = index * 0.09
            add(hit - 2, "item.trident.throw", 0.19 if number != 5 else 0.24,
                0.86 + pitch_offset, "blade-acceleration")
            add(hit, "entity.player.attack.sweep", sweep_volume,
                sweep_pitch + pitch_offset, "broad-cut")

        return sorted(out, key=lambda entry: entry["tick"])

    if name == "skill_left":
        activation = clip["activation_tick"]
        add(0, "block.respawn_anchor.charge", 0.18, 0.63, "shell-charge")
        add(3, "block.amethyst_block.resonate", 0.09, 0.68, "crystal-pressure")
        add(activation - 3, "item.trident.throw", 0.23, 0.74, "upward-draw")
        add(activation, "entity.breeze.wind_burst", 0.39, 0.74, "shell-opening")
        add(activation, "entity.player.attack.sweep", 0.31, 0.69, "ring-expansion")
        add(activation + 4, "block.amethyst_block.resonate", 0.085, 0.67,
            "settled-crystal-tail")

    elif name == "skill_right":
        activation = clip["activation_tick"]
        add(0, "entity.breeze.slide", 0.22, 0.64, "dive-inhale")
        add(activation - 3, "item.trident.throw", 0.29, 0.75, "dive-draw")
        add(activation, "entity.breeze.wind_burst", 0.44, 0.83, "dash-pressure")
        add(activation, "entity.enderman.teleport", 0.18, 0.69, "rift-transition")

    elif name == "skill_right_end":
        # This clip has no damage or activation cue: the authored settle is
        # frame four. End the glide with air instead of a false contact hit.
        add(1, "entity.breeze.slide", 0.21, 0.73, "glide-release")
        add(4, "entity.player.attack.sweep", 0.30, 0.81, "settle-sweep")

    elif name == "burst_jin":
        # Existing datapack meaning: Jin is the compact somersault/buff.
        activation = clip["activation_tick"]
        add(0, "block.respawn_anchor.charge", 0.22, 0.58, "empowerment-draw")
        add(3, "block.amethyst_block.resonate", 0.11, 0.64, "compressed-crystal")
        add(activation - 3, "entity.breeze.slide", 0.28, 0.69, "somersault-wind")
        add(activation, "entity.player.attack.sweep", 0.45, 0.68, "ring-cut")
        add(activation, "entity.breeze.wind_burst", 0.44, 0.68, "empowerment-pressure")
        add(activation + 3, "block.amethyst_block.resonate", 0.10, 0.74,
            "empowerment-tail")

    elif name == "burst_metsu":
        # Existing datapack meaning: Metsu is the large rift and six hits.
        # The authored cut cues indicate motion only. Actual damage provides
        # its own short thud, including cuts that catch more than one enemy.
        add(0, "block.respawn_anchor.charge", 0.27, 0.57, "rift-charge")
        add(10, "block.amethyst_block.resonate", 0.13, 0.62, "orbiting-crystals")
        add(19, "entity.breeze.slide", 0.23, 0.65, "rift-contraction")
        add(hits[0] - 3, "item.trident.throw", 0.31, 0.69, "opening-draw")
        for index, hit in enumerate(hits[:-1]):
            # The two-tick spacing stays clear without repeated impact or
            # brittle shattering layered over every visual slash.
            add(hit, "entity.player.attack.sweep", 0.40 + index * 0.018,
                0.78 + index * 0.055, "rift-cut")
        final_hit = hits[-1]
        add(final_hit - 1, "item.trident.throw", 0.29, 0.68, "final-thrust-draw")
        add(final_hit, "entity.generic.explode", 0.53, 0.72, "rift-collapse-body")
        add(final_hit, "entity.player.attack.sweep", 0.54, 0.61, "rift-collapse-cut")
        add(final_hit + 3, "block.amethyst_block.resonate", 0.105, 0.63,
            "rift-crystal-tail")

    elif name == "sheathe":
        # Idle put-away: every layer sits far below the attacks (air and soft
        # crystal only, no shattering). The dissolve itself stays nearly
        # silent; the shimmer returns when the sword re-forms on her back.
        add(6, "entity.breeze.slide", 0.05, 1.6, "lift-air")
        add(11, "item.armor.equip_diamond", 0.16, 1.7, "point-down-tap")
        add(24, "entity.player.attack.sweep", 0.16, 1.5, "wheel-whoosh")
        add(30, "entity.breeze.slide", 0.12, 1.4, "raise-flick")
        add(38, "block.amethyst_block.resonate", 0.07, 1.4, "float-shimmer")
        add(40, "entity.breeze.slide", 0.06, 1.9, "float-turn")
        add(43, "entity.breeze.slide", 0.04, 2.0, "dissolve-breath")
        add(48, "block.enchantment_table.use", 0.12, 1.6, "back-reform-shimmer")

    return sorted(out, key=lambda entry: entry["tick"])
