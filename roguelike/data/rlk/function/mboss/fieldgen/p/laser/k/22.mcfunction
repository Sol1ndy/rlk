# laser clock 22
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/laser_fire {len:3.74}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/laser_fire {len:3.74}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/p/laser_spot
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/p/laser_spot
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/laser_fire
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] run function rlk:mboss/hz/resize {r:28,r0:0,w:10}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] run function rlk:mboss/hz/resize {r:28,r0:0,w:10}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/snd/laser_loop
