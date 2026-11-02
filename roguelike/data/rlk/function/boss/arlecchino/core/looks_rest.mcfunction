# The rest looks between casts (@s = body): wings folded, the scythe edge normal, the scythe(s) in hand.
function rlk:boss/arlecchino/rig_stub/look/wings/off
function rlk:boss/arlecchino/rig_stub/look/glow/normal
function rlk:boss/arlecchino/rig_stub/look/weapon_r/hand
execute if score #ph kn matches ..4 run function rlk:boss/arlecchino/rig_stub/look/weapon_l/gone
execute if score #ph kn matches 5.. run function rlk:boss/arlecchino/rig_stub/look/weapon_l/hand
