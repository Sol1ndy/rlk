"""Arlecchino's layered scythe/polearm score, made from vanilla events only.

The reference's visual rhythm informs the gesture: a low cutting rush, a clear
edge at the authored damage frame, then a short decay. Actual body contact is
owned by combat/confirmed_hit_sound, never by a swing frame. No recording is used.

Normal attacks run at 150% authored speed. Their compact envelopes leave space
between cuts, especially the two N4 contacts. Explosions are reserved for skill
and burst, and there is no recurring bell, ambient loop, or music bed.
"""

from __future__ import annotations


# body pitch, blade pitch, impact pitch, gain: descent/finale have more mass,
# while the first half of the spinning double cut has a lighter preparation.
NORMAL_PROFILES = {
    1: (0.69, 1.08, 0.78, 0.96),
    2: (0.61, 0.96, 0.68, 1.00),
    3: (0.66, 1.02, 0.74, 0.96),
    4: (0.63, 1.02, 0.74, 0.92),
    5: (0.58, 0.91, 0.70, 1.03),
    6: (0.55, 0.88, 0.63, 1.10),
}


def timeline(name: str, clip: dict) -> list[dict]:
    """Return frame-addressed vanilla components; never change combat timing."""
    if clip.get("loop", False) or clip.get("audio", True) is False:
        return []

    out: list[dict] = []
    last = max(0, int(clip["length"]) - 1)

    def add(tick: int, event: str, volume: float, pitch: float, layer: str) -> None:
        out.append({
            "tick": min(last, max(0, int(tick))),
            "event": event,
            "volume": round(volume, 3),
            "pitch": round(pitch, 3),
            "layer": layer,
        })

    hits = [int(tick) for tick in clip.get("hit_ticks", [])]
    if name.startswith(("physical_", "infused_")):
        number = int(name.rsplit("_", 1)[1])
        infused = name.startswith("infused_")
        body, blade, impact, gain = NORMAL_PROFILES[number]

        if number == 5:
            # Pole-assisted vault: brief lift, then the actual descending cut.
            add(0, "entity.breeze.slide", 0.11, 0.92, "vault_takeoff_air")

        for index, hit in enumerate(hits):
            light_first = number == 4 and index == 0
            local_gain = gain * (0.80 if light_first else 1.0)
            body_pitch = body + (0.14 if light_first else 0.0)
            blade_pitch = blade + (0.16 if light_first else 0.0)
            impact_pitch = impact + (0.10 if light_first else 0.0)

            # Short sweep provides the mass of the shaft; spear attack provides
            # a sharper moving edge without a tiring metallic bell resonance.
            add(hit - 3, "entity.player.attack.sweep", 0.48 * local_gain,
                body_pitch, "shaft_cutting_rush")
            add(hit, "item.spear.attack", 0.20 * local_gain,
                blade_pitch, "blade_edge_contact")

            if infused:
                # Lower fire rush rides the arc; a low-level hiss finishes the
                # cutting envelope. These are not separate explosions per hit.
                add(hit - 2, "item.firecharge.use", 0.25 * local_gain,
                    max(0.55, body_pitch), "bloodfire_arc")
                add(hit + 2, "block.fire.extinguish", 0.12 * local_gain,
                    0.72 if number == 6 else 0.86, "bloodfire_cut_tail")

    elif name == "skill":
        arrival = int(clip["arrival_tick"])
        hit = hits[0]
        add(0, "item.firecharge.use", 0.26, 0.64, "ash_entry_ignition")
        add(arrival - 3, "entity.breeze.slide", 0.18, 0.68, "entry_rush_body")
        add(arrival, "entity.player.attack.sweep", 0.48, 0.58, "entry_scythe_rush")
        add(arrival, "item.spear.attack", 0.23, 0.89, "entry_scythe_edge")
        # One compact delayed ground eruption, distinct from the entry cut.
        add(hit - 1, "item.firecharge.use", 0.26, 0.58, "thorn_flare")
        add(hit, "entity.generic.explode", 0.34, 0.77, "thorn_eruption_body")
        add(hit, "entity.blaze.shoot", 0.30, 0.63, "thorn_flame_release")
        add(hit, "block.heavy_core.hit", 0.17, 0.65, "ground_pressure_contact")
        add(hit + 3, "block.fire.extinguish", 0.18, 0.75, "ash_decay")

    elif name == "burst":
        hit = hits[0]
        # A sparse dark preparation and rising fire leave room for one main
        # blast. No ambient fire loop, monster voice, or repeated explosion.
        add(0, "block.respawn_anchor.charge", 0.26, 0.58, "dark_charge")
        add(max(1, hit - 22), "item.firecharge.use", 0.23, 0.62, "raised_hand_fire")
        add(hit - 10, "entity.breeze.charge", 0.17, 0.68, "gathering_pressure")
        add(hit - 3, "entity.player.attack.sweep", 0.58, 0.55, "cross_release_whoosh")
        add(hit, "entity.generic.explode", 0.80, 0.67, "main_blast_body")
        add(hit, "item.mace.smash_ground_heavy", 0.34, 0.73, "main_blast_low_pressure")
        add(hit, "entity.blaze.shoot", 0.45, 0.59, "infernal_fire_release")
        add(hit + 2, "block.fire.extinguish", 0.24, 0.64, "hot_air_decay")
        add(hit + 7, "block.heavy_core.hit", 0.13, 0.57, "last_ash_fragment")

    return sorted(out, key=lambda component: component["tick"])
