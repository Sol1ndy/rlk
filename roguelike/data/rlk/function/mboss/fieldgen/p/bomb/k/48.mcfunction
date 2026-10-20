# bomb clock 48
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated ~ 0 positioned ^-1.048 ^ ^2.253 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/bomb_drop {h:3.483}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~3.483 ~ run function rlk:mboss/fieldgen/fx/snd/bomb_drop
execute at @s rotated as @s rotated ~ 0 positioned ~ ~3.483 ~ run function rlk:mboss/fieldgen/fx/snd/bomb_fall
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 11
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated ~ 0 positioned ^1.048 ^ ^2.253 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:13,tell:10,dmg:150}
