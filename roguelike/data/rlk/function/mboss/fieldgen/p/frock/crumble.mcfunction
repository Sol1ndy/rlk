# The clip end: every unthrown slab crumbles where it hovers.
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s] at @s positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/slab_impact
kill @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s]
function rlk:mboss/fieldgen/fx/snd/debris_land
playsound minecraft:block.piston.contract hostile @a[tag=player] ~ ~ ~ 0.5 0.9 0.17
