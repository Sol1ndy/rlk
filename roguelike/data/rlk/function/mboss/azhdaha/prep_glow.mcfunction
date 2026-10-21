# The entrance stele glow (every 10 t while its glyph props live; uninstall clears the schedule).
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_az_glyph,limit=1] run return 0
execute in minecraft:overworld positioned -3.5 204.6 15.4 run function rlk:mboss/azhdaha/fx/p/glyph_glow
execute in minecraft:overworld run particle minecraft:wax_on -3.5 204.6 15.4 0.25 0.6 0.1 0 2 force @a[tag=player]
schedule function rlk:mboss/azhdaha/prep_glow 10t replace
