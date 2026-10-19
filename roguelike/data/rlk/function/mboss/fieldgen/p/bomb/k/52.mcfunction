# bomb clock 52
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated ~ 0 positioned ^1.048 ^ ^2.253 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/bomb_drop {h:3.483}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~3.483 ~ run function rlk:mboss/fieldgen/fx/snd/bomb_drop
