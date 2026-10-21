execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/rear_iai
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/verdict
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/snd/iai_charge
execute if score @s rdTime matches 0 at @s rotated as @s run execute positioned ~ ~1.2 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 0 at @s rotated as @s run execute rotated ~180 0 run function rlk:boss/raiden/hazard/new {k:3,a:12000,b:800,c:0,d:0,e:0,f:0,tol:300,tell:14,dmg:15,life:25,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:4,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 10 at @s rotated as @s run execute rotated ~180 0 run execute positioned ~ ~1 ~ run execute positioned ^ ^ ^1.5 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 14 at @s rotated as @s run execute rotated ~180 0 run function rlk:boss/raiden/fx/crystal_line {len:12}
execute if score @s rdTime matches 30 at @s rotated as @s run function rlk:boss/raiden/finish
