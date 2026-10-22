execute if score @s rdTime matches 0 at @s rotated as @s run scoreboard players set @s rdSgV 0
execute if score @s rdTime matches 0 at @s rotated as @s run execute if entity @e[tag=rlk_body,distance=..10,limit=1] run scoreboard players set @s rdSgV 1
execute if score @s rdTime matches 0 if score @s rdSgV matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^11 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute if score @s rdTime matches 0 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/sg/slow_line
execute if score @s rdTime matches 0 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/disc_cast
execute if score @s rdTime matches 0 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/line/will
execute if score @s rdTime matches 0 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ~ ~1.2 ~ run execute positioned ^ ^ ^0.6 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 5 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 5 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 5 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:1000000,c:1700,d:2000,e:800,f:24,tol:300,tell:1,dmg:9,life:26,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:1,sp:-1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 9 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 9 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 9 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:2000000,c:1700,d:2000,e:800,f:12,tol:300,tell:1,dmg:9,life:14,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:1,sp:-1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 17 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 17 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 17 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:2000000,c:1700,d:2000,e:800,f:12,tol:300,tell:1,dmg:9,life:14,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:1,sp:-1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 26 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/snd/iai_charge
execute if score @s rdTime matches 33 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 33 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 33 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:5,a:1000,b:800000,c:1000,d:375,e:927,f:30,tol:300,tell:1,dmg:16,life:32,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:1,lf:0,fv:0}
execute if score @s rdTime matches 34 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/snd/wave_low
execute if score @s rdTime matches 64 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/finish
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/play/disc_cast
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/line/will
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run execute positioned ~ ~1.2 ~ run execute positioned ^ ^ ^0.6 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 15 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 15 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 15 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:1000000,c:1700,d:2000,e:800,f:24,tol:300,tell:1,dmg:9,life:26,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:1,sp:-1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 19 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 19 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 19 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:2000000,c:1700,d:2000,e:800,f:12,tol:300,tell:1,dmg:9,life:14,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:1,sp:-1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 27 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 27 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 27 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:7,a:500,b:2000000,c:1700,d:2000,e:800,f:12,tol:300,tell:1,dmg:9,life:14,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:1,sp:-1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 36 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/fx/snd/iai_charge
execute if score @s rdTime matches 43 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 43 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 43 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:5,a:1000,b:800000,c:1000,d:375,e:927,f:30,tol:300,tell:1,dmg:16,life:32,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:1,lf:0,fv:0}
execute if score @s rdTime matches 44 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/fx/snd/wave_low
execute if score @s rdTime matches 74 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/finish
