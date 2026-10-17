# @s = body: every star husk, then the glyphs (growth over the timer).
execute as @e[type=minecraft:husk,tag=rlk_mb_gd_star] at @s run function rlk:mboss/guardian/star/one
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_starv] at @s run function rlk:mboss/guardian/star/vis_tick
