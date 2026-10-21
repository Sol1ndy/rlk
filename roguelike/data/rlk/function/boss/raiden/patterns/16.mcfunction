# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_iai
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/fx/iai_charge
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:1,a:12000,b:0,c:0,d:0,e:151290000,f:0,tol:300,tell:21,dmg:30,life:32,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 10 at @s rotated as @s run execute positioned ^ ^1.2 ^1.2 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches ..21 run return 0
execute if score @s rdTime matches 22 at @s rotated as @s run function rlk:boss/raiden/fx/snd/iai_hit
execute if score @s rdTime matches 23 at @s rotated as @s run function rlk:boss/raiden/fx/crystal_ring {r:6}
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/finish
