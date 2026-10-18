# laser clock 4
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 run function rlk:mboss/fieldgen/fx/p/laser_charge
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 run function rlk:mboss/fieldgen/fx/p/laser_charge
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/laser_charge
