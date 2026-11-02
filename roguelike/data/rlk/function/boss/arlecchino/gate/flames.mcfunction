# Every 10 t while the gravestone anchor exists (room/clear kills it; uninstall clears the schedule): crimson flames.
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1] run return 0
execute at @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1] run particle minecraft:crimson_spore ~ ~0.3 ~ 0.25 0.3 0.25 0 6
execute at @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1] run particle minecraft:flame ~ ~0.2 ~ 0.15 0.2 0.15 0.01 3
execute at @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1] run particle minecraft:dust{color:[0.75,0.05,0.12],scale:1.2} ~ ~0.4 ~ 0.2 0.35 0.2 0 4
schedule function rlk:boss/arlecchino/gate/flames 10t replace
