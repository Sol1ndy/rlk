# @s = an organism: its display, a 양육's links, itself (no rewards: aux kills pay none).
scoreboard players operation #apO mb = @s apOI
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_om] if score @s apOI = #apO mb run kill @s
execute if score @s apK matches 2 run tag @e[type=minecraft:husk,tag=rlk_mb_ap_basic] remove rlk_mb_ap_buff
execute if score @s apK matches 2 run tag @e[type=minecraft:husk,tag=rlk_mb_ap_basic] remove rlk_mb_ap_imm
kill @s
