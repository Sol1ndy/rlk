# Fail +15: two cube chains fly from the stars into her chest; the glyphs go.
execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 run function rlk:mboss/guardian/fx/absorb_line
kill @e[type=minecraft:text_display,tag=rlk_mb_gd_starv]
