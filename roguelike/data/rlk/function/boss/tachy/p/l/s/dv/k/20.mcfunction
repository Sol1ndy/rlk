# L stage dv tick 20
execute at @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] run function rlk:boss/tachy/fx/p/bolt
execute at @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] positioned ~ ~0.1 ~ run function rlk:boss/tachy/fx/p/shock_ring {r:55}
execute at @s run function rlk:boss/tachy/fx/snd/shock
