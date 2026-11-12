# spiral #apq35T 55
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p35d,scores={apL=7..12}] at @s run function rlk:boss/apep/p/spiral/land
kill @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=7..12}]
execute at @s run function rlk:boss/apep/fx/snd/q5_impact
