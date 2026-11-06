# The slab cap (2 slab hits) is reached: slab 3 crumbles instead of being thrown.
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=3},limit=1] at @s positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/slab_impact
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=3},limit=1] at @s run function rlk:mboss/fieldgen/fx/snd/debris_land
kill @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=3},limit=1]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12t2]
