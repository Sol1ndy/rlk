execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/disc_cast
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/will
execute if score @s rdTime matches 0 at @s rotated as @s run execute positioned ~ ~1.2 ~ run execute positioned ^ ^ ^0.6 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 5 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 5 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 5 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:1300000,c:1700,d:2000,e:800,f:19,tol:300,tell:1,dmg:9,life:21,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 9 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 9 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 9 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:2000000,c:1700,d:2000,e:800,f:12,tol:300,tell:1,dmg:9,life:14,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 17 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 17 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 17 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:2000000,c:1700,d:2000,e:800,f:12,tol:300,tell:1,dmg:9,life:14,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 26 at @s rotated as @s run function rlk:boss/raiden/fx/snd/iai_charge
execute if score @s rdTime matches 33 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 33 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 33 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:5,a:1000,b:800000,c:1000,d:375,e:927,f:30,tol:300,tell:1,dmg:16,life:32,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:1,det:1,lf:0,fv:0}
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/fx/snd/wave_low
execute if score @s rdTime matches 64 at @s rotated as @s run function rlk:boss/raiden/finish
