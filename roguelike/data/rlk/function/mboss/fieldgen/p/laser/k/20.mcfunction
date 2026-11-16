# laser clock 20
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/aim_line {len:3.74}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/aim_line {len:3.74}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.5 1.9 0.17
