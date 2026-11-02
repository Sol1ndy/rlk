# Hook uninstall (no executor; every enabled module): the kit, the rig, the module entities, the gate flames chain,
# objective kn, storage core.*.
function rlk:boss/arlecchino/fx/uninstall
function rlk:boss/arlecchino/rig/uninstall
kill @e[tag=rlk_kn_p]
kill @e[tag=rlk_kn_part]
kill @e[tag=rlk_kn_prop]
kill @e[tag=rlk_kn_fx]
kill @e[tag=rlk_kn_anchor]
kill @e[type=minecraft:item,tag=rlk_kn_orb]
kill @e[tag=rlk_kn_grave]
kill @e[tag=rlk_kn_wisp]
schedule clear rlk:boss/arlecchino/gate/flames
scoreboard objectives remove kn
data remove storage rlk:kn core
data remove storage rlk:kn p2
