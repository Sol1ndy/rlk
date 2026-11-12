execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/combo5
execute if score @s rdTime matches 0 at @s rotated as @s run execute positioned ~ ~1.1 ~ run execute positioned ^ ^ ^0.8 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 0 at @s rotated as @s run scoreboard players add #rdGrpSerial rd 1
execute if score @s rdTime matches 0 at @s rotated as @s run execute rotated ~-25 0 run function rlk:boss/raiden/hazard/new {k:3,a:6000,b:600,c:0,d:0,e:0,f:0,tol:300,tell:12,dmg:8,life:23,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:7,sm:3,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 0 at @s rotated as @s run execute rotated ~25 0 run function rlk:boss/raiden/hazard/new {k:3,a:6000,b:600,c:0,d:0,e:0,f:0,tol:300,tell:12,dmg:8,life:23,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:7,sm:3,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 4 at @s rotated as @s run execute positioned ^ ^ ^0.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 5 at @s rotated as @s run execute positioned ^ ^ ^0.75 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 12 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 12 at @s rotated as @s run execute rotated ~20 0 run function rlk:boss/raiden/hazard/new {k:3,a:9000,b:750,c:0,d:0,e:0,f:0,tol:300,tell:10,dmg:8,life:21,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:1,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 22 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 22 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 22 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 22 at @s rotated as @s run execute positioned ^ ^ ^2 run function rlk:boss/raiden/hazard/new {k:1,a:2500,b:0,c:0,d:0,e:7840000,f:0,tol:300,tell:12,dmg:9,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 34 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 34 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 34 at @s rotated as @s run execute rotated ~-20 0 run function rlk:boss/raiden/hazard/new {k:3,a:10000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:16,dmg:12,life:27,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:2,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 50 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 50 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 50 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 50 at @s rotated as @s run execute positioned ^ ^ ^2.5 run function rlk:boss/raiden/hazard/new {k:1,a:3000,b:0,c:0,d:0,e:10890000,f:0,tol:300,tell:14,dmg:13,life:25,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 74 at @s rotated as @s run function rlk:boss/raiden/finish
