# bomb clock 10
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p1e,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/p/ports_glow
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/bomb_port
execute at @s rotated as @s rotated ~ 0 positioned ^1.048 ^3.483 ^2.253 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
execute at @s rotated as @s rotated ~ 0 positioned ^2.529 ^3.891 ^0.829 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
execute at @s rotated as @s rotated ~ 0 positioned ^2.529 ^4.469 ^-1.185 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
execute at @s rotated as @s rotated ~ 0 positioned ^1.048 ^4.877 ^-2.609 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
execute at @s rotated as @s rotated ~ 0 positioned ^-1.048 ^4.877 ^-2.609 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
execute at @s rotated as @s rotated ~ 0 positioned ^-2.529 ^4.469 ^-1.185 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
execute at @s rotated as @s rotated ~ 0 positioned ^-2.529 ^3.891 ^0.829 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
execute at @s rotated as @s rotated ~ 0 positioned ^-1.048 ^3.483 ^2.253 run function rlk:mboss/fieldgen/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.75,move:"0f,0f,0f",life:4,fade:2,col:14793854}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 13
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated ~ 0 positioned ^-1.048 ^ ^2.253 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:13,tell:10,dmg:150}
