execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/p_rear
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/twirl {life:16}
execute if score @s rdTime matches 0 at @s rotated as @s run execute rotated ~180 0 run function rlk:boss/raiden/hazard/new {k:2,a:4200,b:5800,c:985,d:-174,e:37210000,f:15210000,tol:300,tell:16,dmg:10,life:27,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:5,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 0 at @s rotated as @s run execute rotated ~180 0 run function rlk:boss/raiden/hazard/new {k:2,a:4200,b:5800,c:985,d:-174,e:37210000,f:15210000,tol:300,tell:26,dmg:12,life:37,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:5,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 12 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 36 at @s rotated as @s run function rlk:boss/raiden/finish
