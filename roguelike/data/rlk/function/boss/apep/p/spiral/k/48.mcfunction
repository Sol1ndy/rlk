# spiral #apq35T 48
scoreboard players set #apq35R mb 1
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=1..6}] at @s run function rlk:boss/apep/p/spiral/fly
execute at @s run function rlk:boss/apep/fx/snd/q5_launch
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=7..12}] run data merge entity @s {teleport_duration:1}
scoreboard players set #apq35R mb 7
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=7..12}] at @s run function rlk:boss/apep/p/spiral/fly
