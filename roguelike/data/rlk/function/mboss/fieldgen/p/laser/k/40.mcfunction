# laser clock 40
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/p/spark
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
