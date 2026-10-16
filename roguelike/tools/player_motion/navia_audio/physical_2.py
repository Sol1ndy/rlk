"""Navia physical_2 sound layers (owner: na12). Vanilla sound events only; see player_motion/audio_navia.py
for the layer format and for the sounds gameplay already plays (never double those).

Timeline from v2 A2 / v3 §7.5 (NA2), offsets from the contact tick (hit = 6, authored ticks):
- re-cock: a light metallic drag as the blade sinks behind her right foot;
- the rising swing: a duller, higher rush than NA1, then a weak edge just after contact;
- the Geo crystal spikes out of the floor at hit+1 (a brief crystal crackle, never a ringing chime) and a low
  thump under them at hit+2;
- the overhead carry and the skip-hop (air + cloth), then the landing step.
All names are already used in the pack (scratchpad/navia/dp_sound_events.txt).
"""


def timeline(clip: dict) -> list[dict]:
    hit = (clip.get("hit_ticks") or [6])[0]
    return [
        {"tick": 2, "event": "block.chain.hit", "volume": 0.15, "pitch": 1.2, "layer": "re-cock drag"},
        {"tick": hit - 2, "event": "entity.player.attack.sweep", "volume": 0.46, "pitch": 0.8, "layer": "rising rush"},
        {"tick": hit - 1, "event": "item.trident.throw", "volume": 0.16, "pitch": 0.78, "layer": "swing weight"},
        {"tick": hit + 1, "event": "item.spear.attack", "volume": 0.15, "pitch": 0.78, "layer": "edge"},
        {"tick": hit + 1, "event": "block.amethyst_cluster.place", "volume": 0.38, "pitch": 0.9, "layer": "crystal spikes"},
        {"tick": hit + 2, "event": "block.heavy_core.hit", "volume": 0.18, "pitch": 0.7, "layer": "spike thump"},
        {"tick": hit + 2, "event": "entity.player.attack.sweep", "volume": 0.2, "pitch": 1.05, "layer": "overhead carry"},
        {"tick": hit + 3, "event": "item.armor.equip_leather", "volume": 0.16, "pitch": 1.2, "layer": "skip-hop cloth"},
        {"tick": min(hit + 6, clip.get("length", 14)), "event": "block.stone.step", "volume": 0.3, "pitch": 0.9, "layer": "landing"},
    ]
