execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/p_twirl_dash
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/shadow_world
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/twirl {life:15}
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 12 at @s rotated as @s run function rlk:boss/raiden/fx/snd/star
execute if score @s rdTime matches 12 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:11000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:8,dmg:12,life:19,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:4,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 19 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 20 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 21 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 22 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 22 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 22 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 22 at @s rotated as @s run function rlk:boss/raiden/fx/snd/star
execute if score @s rdTime matches 22 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:11000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:10,dmg:12,life:21,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:4,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 31 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 32 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 33 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 34 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 34 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 34 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/fx/snd/star
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:11000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:10,dmg:12,life:21,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:4,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 43 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 44 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 45 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 46 at @s rotated as @s run execute positioned ^ ^ ^2.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 58 at @s rotated as @s run function rlk:boss/raiden/finish
