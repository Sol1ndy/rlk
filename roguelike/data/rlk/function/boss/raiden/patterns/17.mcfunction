# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/goemyeol
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run execute positioned ^ ^2 ^1 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 5 at @s rotated as @s run scoreboard players operation @s rdRigL = @s rdAnim
execute if score @s rdTime matches 5 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_waves
execute if score @s rdTime matches ..7 run return 0
execute if score @s rdTime matches 8 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 8 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 11 at @s rotated as @s run scoreboard players add #rdGrpSerial rd 1
execute if score @s rdTime matches 11 at @s rotated as @s run execute rotated ~-30 0 run function rlk:boss/raiden/hazard/new {k:6,a:2500,b:450000,c:900,d:1000,e:4500,f:48,tol:300,tell:1,dmg:15,life:50,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
execute if score @s rdTime matches 11 at @s rotated as @s run execute rotated ~-15 0 run function rlk:boss/raiden/hazard/new {k:6,a:2500,b:450000,c:900,d:1000,e:4500,f:48,tol:300,tell:1,dmg:15,life:50,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
execute if score @s rdTime matches 11 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:6,a:2500,b:450000,c:900,d:1000,e:4500,f:48,tol:300,tell:1,dmg:15,life:50,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
execute if score @s rdTime matches 11 at @s rotated as @s run execute rotated ~15 0 run function rlk:boss/raiden/hazard/new {k:6,a:2500,b:450000,c:900,d:1000,e:4500,f:48,tol:300,tell:1,dmg:15,life:50,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
execute if score @s rdTime matches 11 at @s rotated as @s run execute rotated ~30 0 run function rlk:boss/raiden/hazard/new {k:6,a:2500,b:450000,c:900,d:1000,e:4500,f:48,tol:300,tell:1,dmg:15,life:50,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
execute if score @s rdTime matches ..11 run return 0
execute if score @s rdTime matches 12 at @s rotated as @s run function rlk:boss/raiden/fx/snd/wave_slab
execute if score @s rdTime matches 45 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 45 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 45 at @s rotated as @s run execute positioned ^ ^1 ^1.5 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 56 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:5,a:2500,b:280000,c:1000,d:643,e:766,f:84,tol:300,tell:1,dmg:20,life:86,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:5,snd:1,nd:0,jp:1,det:1,lf:0,fv:0}
execute if score @s rdTime matches 57 at @s rotated as @s run function rlk:boss/raiden/fx/snd/wave_low
execute if score @s rdTime matches ..73 run return 0
execute if score @s rdTime matches 74 at @s rotated as @s run function rlk:boss/raiden/finish
