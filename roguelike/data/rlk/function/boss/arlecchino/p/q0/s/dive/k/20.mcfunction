# Q0 stage dive tick 20
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/impact_burst {r:30,c:2}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/fx/snd/fall_impact
