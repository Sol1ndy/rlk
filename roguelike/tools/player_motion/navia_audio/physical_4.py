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

Retimed (D11): the ticks below are the original layers pushed through the clip time-warp (playback 100,
Genshin cadence and recovery). This literal list is the source now; edit it directly."""

LAYERS = [
    {"tick": 0, "event": "block.amethyst_block.chime", "volume": 0.3, "pitch": 1.6, "layer": "parasol appears"},
    {"tick": 1, "event": "item.armor.equip_leather", "volume": 0.3, "pitch": 1.3, "layer": "parasol drawn"},
    {"tick": 2, "event": "entity.player.attack.sweep", "volume": 0.15, "pitch": 1.7, "layer": "swing up"},
    {"tick": 5, "event": "block.amethyst_block.chime", "volume": 0.25, "pitch": 1.9, "layer": "load shimmer"},
    {"tick": 5, "event": "item.crossbow.loading_middle", "volume": 0.35, "pitch": 1.3, "layer": "load"},
    {"tick": 7, "event": "block.note_block.chime", "volume": 0.12, "pitch": 0.5, "layer": "load tone"},
    {"tick": 8, "event": "item.crossbow.loading_end", "volume": 0.3, "pitch": 1.5, "layer": "cocked"},
    {"tick": 9, "event": "entity.player.attack.sweep", "volume": 0.18, "pitch": 1.3, "layer": "shoulder swing"},
    {"tick": 11, "event": "entity.player.attack.sweep", "volume": 0.35, "pitch": 1.4, "layer": "whip to aim"},
    {"tick": 12, "event": "entity.firework_rocket.blast", "volume": 0.6, "pitch": 0.8, "layer": "shot body"},
    {"tick": 12, "event": "item.crossbow.shoot", "volume": 0.45, "pitch": 0.65, "layer": "shot crack"},
    {"tick": 13, "event": "entity.generic.explode", "volume": 0.18, "pitch": 1.7, "layer": "shot tail"},
    {"tick": 14, "event": "entity.breeze.wind_burst", "volume": 0.45, "pitch": 0.85, "layer": "launch"},
    {"tick": 14, "event": "block.amethyst_cluster.break", "volume": 0.45, "pitch": 0.8, "layer": "eruption"},
    {"tick": 15, "event": "entity.player.attack.sweep", "volume": 0.3, "pitch": 0.7, "layer": "up-swing"},
    {"tick": 16, "event": "item.trident.riptide_1", "volume": 0.2, "pitch": 1.4, "layer": "flip whirl"},
    {"tick": 17, "event": "block.amethyst_block.break", "volume": 0.3, "pitch": 0.9, "layer": "eruption crash"},
    {"tick": 21, "event": "item.armor.equip_elytra", "volume": 0.4, "pitch": 1.3, "layer": "canopy opens"},
    {"tick": 22, "event": "block.note_block.flute", "volume": 0.1, "pitch": 0.54, "layer": "float tone low"},
    {"tick": 22, "event": "block.note_block.flute", "volume": 0.08, "pitch": 0.81, "layer": "float tone high"},
    {"tick": 28, "event": "block.stone.step", "volume": 0.35, "pitch": 0.9, "layer": "landing"},
    {"tick": 28, "event": "item.armor.equip_leather", "volume": 0.22, "pitch": 1.1, "layer": "landing cloth"},
    {"tick": 32, "event": "entity.breeze.slide", "volume": 0.12, "pitch": 1.3, "layer": "canopy twirl"},
    {"tick": 36, "event": "item.crossbow.loading_end", "volume": 0.28, "pitch": 1.6, "layer": "parasol closes"},
    {"tick": 42, "event": "block.amethyst_block.resonate", "volume": 0.2, "pitch": 1.6, "layer": "parasol dissolves"},
    {"tick": 43, "event": "item.armor.equip_iron", "volume": 0.25, "pitch": 1.2, "layer": "halberd re-forms"},
    {"tick": 48, "event": "block.amethyst_block.chime", "volume": 0.15, "pitch": 1.4, "layer": "re-form glint"},
]


def timeline(clip: dict) -> list[dict]:
    length = int(clip.get("length", 62))
    return [dict(layer) for layer in LAYERS if 0 <= layer["tick"] <= length]
