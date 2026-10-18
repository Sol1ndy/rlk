# bomb clock 10
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p1e,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/p/ports_glow
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/bomb_port
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 13
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated ~ 0 positioned ^-1.05 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:13,tell:10,dmg:80}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated ~ 0 positioned ^-1.05 ^ ^ positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/tele/disc {r:13,tell:10,el:5,hold:3}
