execute if score @s rdTime matches 0 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^7 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/sg/slow_line
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/rig/play/p_lance
execute if score @s rdTime matches 16 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 16 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 16 at @s rotated as @s run execute positioned ~ ~2.2 ~ run execute positioned ^ ^ ^1 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 16 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/new {k:1,a:2000,b:0,c:0,d:0,e:5290000,f:0,tol:300,tell:8,dmg:14,life:19,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:2,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/finish
