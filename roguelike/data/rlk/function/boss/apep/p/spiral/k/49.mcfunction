# spiral #apq35T 49
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p35d,scores={apL=1..6}] at @s run function rlk:boss/apep/p/spiral/land
kill @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=1..6}]
execute at @s run function rlk:boss/apep/fx/snd/q5_impact
scoreboard players set #apq35R mb 6
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=7..12}] at @s run function rlk:boss/apep/p/spiral/fly
