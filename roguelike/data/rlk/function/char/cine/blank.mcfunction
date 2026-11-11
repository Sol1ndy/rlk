# Internal (@s = the avatar, once per hide): its profile kept in storage rlk:cine av (none: it wears the default skin),
# the skin texture replaced by the fully transparent rlk:skin/blank (tools/build_blank_tex.py writes it into the pack): the
# ghost a spectator would see of the invisible avatar has nothing to draw.
data remove storage rlk:cine av
data modify storage rlk:cine av set from entity @s profile
data modify entity @s profile.texture set value "rlk:skin/blank"
