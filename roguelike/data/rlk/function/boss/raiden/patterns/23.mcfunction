execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/p_zigzag
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/noemyeong
execute if score @s rdTime matches 6 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 6 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:9000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:8,dmg:12,life:19,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:4,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 8 at @s rotated as @s run execute positioned ~ ~1.2 ~ run execute positioned ^ ^ ^0.6 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 11 at @s rotated as @s run execute unless entity @e[tag=rlk_body,distance=..2.5,limit=1] run execute positioned ^ ^ ^2 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 12 at @s rotated as @s run execute unless entity @e[tag=rlk_body,distance=..2.5,limit=1] run execute positioned ^ ^ ^2 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 13 at @s rotated as @s run execute unless entity @e[tag=rlk_body,distance=..2.5,limit=1] run execute positioned ^ ^ ^2 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 14 at @s rotated as @s run execute unless entity @e[tag=rlk_body,distance=..2.5,limit=1] run execute positioned ^ ^ ^2 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 22 at @s rotated as @s run execute positioned ~ ~1 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 22 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:1,a:4500,b:0,c:0,d:0,e:23040000,f:0,tol:300,tell:12,dmg:6,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:5000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:12,dmg:14,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:4,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 64 at @s rotated as @s run function rlk:boss/raiden/finish
