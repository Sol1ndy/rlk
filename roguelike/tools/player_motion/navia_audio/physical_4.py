"""Navia physical_4 sound layers (owner: na4). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

Timeline after v2 §6-§7 (A7-A12) and v3 §7 (A13-A16, A34-A38), on the clip's authored ticks: the parasol
appears with a small shimmer, is "loaded" (airy shimmer, one soft tone, a cocking click), swung over the left
shoulder and whipped down to aim, fires on the hit tick (a short muffled boom-crack: the shot is the clip's own
sound, normal attacks have no gameplay shot sound; the confirmed-hit thud stays with combat), launches her with a
wind burst over the crystal eruption, whirls through the backflip, opens the canopy with a fabric snap, floats
(one soft two-tone note, not a loop), lands with a light step and cloth, twirls, clicks shut, dissolves, and the
halberd re-forms on the back with a short metal settle and a faint chime.

Every event is either in scratchpad/navia/dp_sound_events.txt (already used by the pack) or a well-known vanilla
id: item.crossbow.shoot, item.armor.equip_elytra and block.note_block.flute are vanilla but new to the pack.
"""

LAYERS = [
    # parasol appears at the right hip, swung up before the right shoulder
    {"tick": 0, "event": "block.amethyst_block.chime", "volume": 0.3, "pitch": 1.6, "layer": "parasol appears"},
    {"tick": 1, "event": "item.armor.equip_leather", "volume": 0.3, "pitch": 1.3, "layer": "parasol drawn"},
    {"tick": 2, "event": "entity.player.attack.sweep", "volume": 0.15, "pitch": 1.7, "layer": "swing up"},
    # "load": glint flare, a soft tone (v2 A7 / v3 A14 hum, once) and a cocking click
    {"tick": 4, "event": "block.amethyst_block.chime", "volume": 0.25, "pitch": 1.9, "layer": "load shimmer"},
    {"tick": 4, "event": "item.crossbow.loading_middle", "volume": 0.35, "pitch": 1.3, "layer": "load"},
    {"tick": 5, "event": "block.note_block.chime", "volume": 0.12, "pitch": 0.5, "layer": "load tone"},
    {"tick": 6, "event": "item.crossbow.loading_end", "volume": 0.3, "pitch": 1.5, "layer": "cocked"},
    # over the left shoulder, then the whip down to aim
    {"tick": 7, "event": "entity.player.attack.sweep", "volume": 0.18, "pitch": 1.3, "layer": "shoulder swing"},
    {"tick": 9, "event": "entity.player.attack.sweep", "volume": 0.35, "pitch": 1.4, "layer": "whip to aim"},
    # the shot (hit tick 10): muffled boom + crack, short tail
    {"tick": 10, "event": "entity.firework_rocket.blast", "volume": 0.6, "pitch": 0.8, "layer": "shot body"},
    {"tick": 10, "event": "item.crossbow.shoot", "volume": 0.45, "pitch": 0.65, "layer": "shot crack"},
    {"tick": 11, "event": "entity.generic.explode", "volume": 0.18, "pitch": 1.7, "layer": "shot tail"},
    # launch: wind burst, crystal eruption, the parasol swung overhead, the backflip whirl
    {"tick": 12, "event": "entity.breeze.wind_burst", "volume": 0.45, "pitch": 0.85, "layer": "launch"},
    {"tick": 12, "event": "block.amethyst_cluster.break", "volume": 0.45, "pitch": 0.8, "layer": "eruption"},
    {"tick": 13, "event": "entity.player.attack.sweep", "volume": 0.3, "pitch": 0.7, "layer": "up-swing"},
    {"tick": 14, "event": "item.trident.riptide_1", "volume": 0.2, "pitch": 1.4, "layer": "flip whirl"},
    {"tick": 15, "event": "block.amethyst_block.break", "volume": 0.3, "pitch": 0.9, "layer": "eruption crash"},
    # the canopy opens at the apex; one soft two-tone note under the float (v3 A36 401 + 602 Hz)
    {"tick": 19, "event": "item.armor.equip_elytra", "volume": 0.4, "pitch": 1.3, "layer": "canopy opens"},
    {"tick": 21, "event": "block.note_block.flute", "volume": 0.1, "pitch": 0.54, "layer": "float tone low"},
    {"tick": 21, "event": "block.note_block.flute", "volume": 0.08, "pitch": 0.81, "layer": "float tone high"},
    # landing on the left foot, back kick and canopy twirl, close, gold dissolve
    {"tick": 25, "event": "block.stone.step", "volume": 0.35, "pitch": 0.9, "layer": "landing"},
    {"tick": 25, "event": "item.armor.equip_leather", "volume": 0.22, "pitch": 1.1, "layer": "landing cloth"},
    {"tick": 26, "event": "entity.breeze.slide", "volume": 0.12, "pitch": 1.3, "layer": "canopy twirl"},
    {"tick": 27, "event": "item.crossbow.loading_end", "volume": 0.28, "pitch": 1.6, "layer": "parasol closes"},
    {"tick": 28, "event": "block.amethyst_block.resonate", "volume": 0.2, "pitch": 1.6, "layer": "parasol dissolves"},
    # the halberd re-forms on the back
    {"tick": 29, "event": "item.armor.equip_iron", "volume": 0.25, "pitch": 1.2, "layer": "halberd re-forms"},
    {"tick": 31, "event": "block.amethyst_block.chime", "volume": 0.15, "pitch": 1.4, "layer": "re-form glint"},
]


def timeline(clip: dict) -> list[dict]:
    length = int(clip.get("length", 32))
    return [layer for layer in LAYERS if layer["tick"] <= length]
