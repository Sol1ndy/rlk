# frock clock 33
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=2},limit=1] at @s run function rlk:mboss/fieldgen/p/frock/rise1
function rlk:mboss/fieldgen/p/frock/burst3
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12r] at @s run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~-0.3 ~ 0.5 0.1 0.5 0 1 force @a[tag=player]
