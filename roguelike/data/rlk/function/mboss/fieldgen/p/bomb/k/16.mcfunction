# bomb clock 16
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated ~ 0 positioned ^0 ^ ^ positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/bomb_drop {h:3.8}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~3.8 ~ run function rlk:mboss/fieldgen/fx/snd/bomb_drop
