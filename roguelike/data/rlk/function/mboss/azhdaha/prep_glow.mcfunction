# The entrance stele glow (every 10 t while its glyph props live; uninstall clears the schedule).
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_az_glyph,limit=1] run return 0
schedule function rlk:mboss/azhdaha/prep_glow 10t replace
