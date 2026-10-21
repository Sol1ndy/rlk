# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_seed
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/fx/twirl {life:8}
execute if score @s rdTime matches 8 at @s rotated as @s run function rlk:boss/raiden/tm/shadow/seed
execute if score @s rdTime matches 9 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_seed] at @e[tag=rlk_body,limit=1] run tp @s ~ ~0.4 ~
execute if score @s rdTime matches ..11 run return 0
execute if score @s rdTime matches 12 at @s rotated as @s run kill @e[tag=rlk_rd_tm_seed]
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/new {k:8,a:1500,b:320000,c:0,d:0,e:3240000,f:0,tol:300,tell:16,dmg:4,life:57,ev:20,max:0,grp:0,dk:6,dl:0,kb:0,sv:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0.32}
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/fx/crystal
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @e[tag=rlk_rd_hazard,scores={rdHK=8},limit=1] run function rlk:boss/raiden/fx/snd/shadow_loop
execute if score @s rdTime matches 32 at @s rotated as @s run execute at @e[tag=rlk_rd_hazard,scores={rdHK=8},limit=1] run function rlk:boss/raiden/fx/snd/shadow_loop
execute if score @s rdTime matches 52 at @s rotated as @s run execute at @e[tag=rlk_rd_hazard,scores={rdHK=8},limit=1] run function rlk:boss/raiden/fx/snd/shadow_loop
execute if score @s rdTime matches ..67 run return 0
execute if score @s rdTime matches 68 at @s rotated as @s run execute at @e[tag=rlk_rd_hazard,scores={rdHK=8},limit=1] run function rlk:boss/raiden/fx/snd/shadow_grow
execute if score @s rdTime matches 69 at @s rotated as @s run function rlk:boss/raiden/tm/shadow/grow
execute if score @s rdTime matches 72 at @s rotated as @s run function rlk:boss/raiden/tm/shadow/palm
execute if score @s rdTime matches 73 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_palm,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,7f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.2f,3.2f,3.2f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdTime matches 77 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_palm,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,7.4f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.2f,3.2f,3.2f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdTime matches 81 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_palm,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,0.3f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.2f,3.2f,3.2f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdTime matches ..83 run return 0
execute if score @s rdTime matches 84 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/shadow_palm
execute if score @s rdTime matches 85 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_palm,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0.7f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.2f,3.2f,3.2f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdTime matches 89 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_palm,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0f,1.2f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdTime matches 95 at @s rotated as @s run kill @e[tag=rlk_rd_tm_palm]
execute if score @s rdTime matches 96 at @s rotated as @s run function rlk:boss/raiden/finish
