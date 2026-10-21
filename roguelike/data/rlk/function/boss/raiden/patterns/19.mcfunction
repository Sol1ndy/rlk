# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_danjeol
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/fx/danjeol_halo
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/line/sever
execute if score @s rdTime matches 16 at @s rotated as @s run function rlk:boss/raiden/fx/danjeol_column
execute if score @s rdTime matches ..23 run return 0
execute if score @s rdTime matches 24 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 24 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 24 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:4,a:0,b:2500,c:0,d:0,e:0,f:0,tol:300,tell:40,dmg:34,life:51,ev:10,max:1,grp:0,dk:5,dl:0,kb:0,sv:8,sm:3,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 24 at @s rotated as @s run function rlk:boss/raiden/fx/snd/danjeol_band
execute if score @s rdTime matches 64 at @s rotated as @s run function rlk:boss/raiden/fx/snd/danjeol_slam
execute if score @s rdTime matches 64 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:9,a:4500,b:0,c:0,d:0,e:23040000,f:0,tol:300,tell:2,dmg:3,life:43,ev:10,max:0,grp:0,dk:0,dl:0,kb:0,sv:9,sm:0,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
execute if score @s rdTime matches ..69 run return 0
execute if score @s rdTime matches 70 at @s rotated as @s run function rlk:boss/raiden/finish
