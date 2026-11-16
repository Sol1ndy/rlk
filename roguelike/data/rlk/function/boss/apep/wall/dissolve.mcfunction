# @s = a wall group: its blocks removed (only the recorded ones that are still barrier), the blades fade.
scoreboard players operation #apX mb = @s apL
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wallb] if score @s apL = #apX mb at @s run function rlk:boss/apep/wall/unput
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade] if score @s apL = #apX mb run function rlk:boss/apep/wall/fade1
execute at @s run function rlk:boss/apep/fx/snd/o4_fade
