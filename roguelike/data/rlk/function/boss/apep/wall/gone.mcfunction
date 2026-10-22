scoreboard players operation #apX mb = @s apL
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade] if score @s apL = #apX mb run kill @s
kill @s
