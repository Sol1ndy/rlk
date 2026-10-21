execute if score @s rdTime matches 0 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^-4.5 ^ ^0 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/rig/play/p_twirl_slam
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/line/return_dust
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/fx/twirl {life:36}
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:1,a:6500,b:0,c:0,d:0,e:46240000,f:0,tol:300,tell:40,dmg:22,life:51,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:1,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 16 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 22 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 28 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 46 at @s rotated as @s run function rlk:boss/raiden/fx/snd/twirl_beat
execute if score @s rdTime matches 48 at @s rotated as @s run execute positioned ~ ~1.8 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 62 at @s rotated as @s run function rlk:boss/raiden/finish
