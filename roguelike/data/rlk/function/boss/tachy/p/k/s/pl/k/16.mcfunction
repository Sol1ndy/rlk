# K stage pl tick 16
execute at @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] run function rlk:boss/tachy/fx/p/bolt
execute at @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] positioned ~ ~0.1 ~ run function rlk:boss/tachy/fx/p/shock_ring {r:35}
execute at @s run function rlk:boss/tachy/fx/snd/plunge
