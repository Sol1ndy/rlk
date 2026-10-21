# Phase 1, as the boss: the transformation timeline on rdTime (plan B.2 row T).
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/transform
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..1.5] at @s run function rlk:boss/raiden/fx/blink_out
execute if score @s rdTime matches 2 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..1.5] run function rlk:boss/raiden/fx/blink_in
execute if score @s rdTime matches 2 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 2 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 19 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:1000000,c:1400,d:0,e:-1000,f:24,tol:300,tell:1,dmg:14,life:26,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches 20 at @s rotated as @s run function rlk:boss/raiden/fx/snd/transform_ring
execute if score @s rdTime matches 24 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/new {k:1,a:1500,b:0,c:0,d:0,e:3240000,f:0,tol:300,tell:20,dmg:16,life:31,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:2,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 24 at @s rotated as @s run execute store result storage rlk:rd tm.rot int 1 run random value 0..359
execute if score @s rdTime matches 24 at @s rotated as @s run function rlk:boss/raiden/tm/t/pillars with storage rlk:rd tm
execute if score @s rdTime matches 24 at @s rotated as @s run function rlk:boss/raiden/fx/snd/transform_pillars
execute if score @s rdTime matches 24 at @s rotated as @s run execute positioned ~ ~9 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 46 at @s rotated as @s run function rlk:boss/raiden/fx/transform_burst
execute if score @s rdTime matches 50 at @s rotated as @s run function rlk:boss/raiden/transform_title
execute if score @s rdTime matches 50 at @s rotated as @s run function rlk:room/raiden/look_tenma
execute if score @s rdTime matches 60 at @s rotated as @s run function rlk:boss/raiden/armor_start
