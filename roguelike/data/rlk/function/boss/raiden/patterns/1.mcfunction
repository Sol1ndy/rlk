execute if score @s rdTime matches 0 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^2.5 ^ ^0 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/sg/slow_line
execute if score @s rdTime matches 6 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 6 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/rig/play/p_4hit
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:2,a:0,b:5500,c:1000,d:0,e:33640000,f:0,tol:300,tell:18,dmg:9,life:29,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:5,sm:2,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 16 at @s rotated as @s run execute positioned ~ ~2.2 ~ run execute positioned ^ ^ ^1 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 28 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 28 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 28 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 28 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:2,a:0,b:5500,c:1000,d:0,e:33640000,f:0,tol:300,tell:10,dmg:9,life:21,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:5,sm:1,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 38 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 38 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 38 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 38 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:6000,b:750,c:0,d:0,e:0,f:0,tol:300,tell:10,dmg:10,life:21,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:3,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 48 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 48 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 48 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 48 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:3000,b:7500,c:2000,d:0,e:0,f:0,tol:300,tell:14,dmg:15,life:25,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:3,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run function rlk:boss/raiden/fx/snd/bomb_tell
execute if score @s rdTime matches 62 at @s rotated as @s run scoreboard players add #rdGrpSerial rd 1
execute if score @s rdTime matches 62 at @s rotated as @s run execute positioned ^-4 ^ ^5.6 run function rlk:boss/raiden/hazard/new {k:1,a:1200,b:0,c:0,d:0,e:2250000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run execute positioned ^-1.6 ^ ^9.8 run function rlk:boss/raiden/hazard/new {k:1,a:1200,b:0,c:0,d:0,e:2250000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run execute positioned ^0.6 ^ ^6.2 run function rlk:boss/raiden/hazard/new {k:1,a:1200,b:0,c:0,d:0,e:2250000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run execute positioned ^3.6 ^ ^8.9 run function rlk:boss/raiden/hazard/new {k:1,a:1200,b:0,c:0,d:0,e:2250000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run execute positioned ^-3.2 ^ ^10.4 run function rlk:boss/raiden/hazard/new {k:1,a:1200,b:0,c:0,d:0,e:2250000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run execute positioned ^1.9 ^ ^10.6 run function rlk:boss/raiden/hazard/new {k:1,a:1200,b:0,c:0,d:0,e:2250000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run execute positioned ^4.2 ^ ^5.4 run function rlk:boss/raiden/hazard/new {k:1,a:1200,b:0,c:0,d:0,e:2250000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 90 at @s rotated as @s run scoreboard players set @s rdSgV 0
execute if score @s rdTime matches 90 at @s rotated as @s run execute unless entity @e[tag=rlk_body,distance=..5,limit=1] store result score #rdSgR rd run random value 0..99
execute if score @s rdTime matches 90 at @s rotated as @s run execute unless entity @e[tag=rlk_body,distance=..5,limit=1] if score #rdSgR rd matches ..59 run scoreboard players set @s rdSgV 1
execute if score @s rdTime matches 90 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 90 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 90 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/play/p_lance
execute if score @s rdTime matches 96 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/finish
execute if score @s rdTime matches 96 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 96 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 96 if score @s rdSgV matches 1 at @s rotated as @s run execute positioned ~ ~2.2 ~ run execute positioned ^ ^ ^1 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 96 if score @s rdSgV matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/new {k:1,a:2000,b:0,c:0,d:0,e:5290000,f:0,tol:300,tell:8,dmg:14,life:19,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:2,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 112 at @s rotated as @s run function rlk:boss/raiden/finish
