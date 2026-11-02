# Every 10 t while the gravestone anchor exists (room/clear kills it; uninstall clears the schedule): crimson flames.
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1] run return 0
execute at @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1] run function rlk:boss/arlecchino/fx/p/gate_flames
schedule function rlk:boss/arlecchino/gate/flames 10t replace
