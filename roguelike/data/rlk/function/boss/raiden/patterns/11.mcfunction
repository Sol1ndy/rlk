# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_combo3
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/cleave_all
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:2,a:2500,b:7500,c:985,d:-174,e:60840000,f:4840000,tol:300,tell:13,dmg:19,life:24,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:5,sm:2,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/fx/snd/glaive_sweep
execute if score @s rdTime matches ..14 run return 0
execute if score @s rdTime matches 15 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 15 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 15 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:2,a:2500,b:7500,c:985,d:-174,e:60840000,f:4840000,tol:300,tell:11,dmg:19,life:22,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:5,sm:1,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 26 at @s rotated as @s run function rlk:boss/raiden/fx/snd/glaive_sweep
execute if score @s rdTime matches 42 at @s rotated as @s run kill @e[tag=rlk_rd_tm_spot]
execute if score @s rdTime matches 42 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_spot"]}
execute if score @s rdTime matches 42 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 42 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 42 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:3000,b:0,c:0,d:0,e:10890000,f:0,tol:300,tell:12,dmg:18,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 42 at @s rotated as @s run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.7 1.3 0.3
execute if score @s rdTime matches ..50 run return 0
execute if score @s rdTime matches 51 at @s rotated as @s run function rlk:boss/raiden/tm/glaive_fly
execute if score @s rdTime matches 52 at @s rotated as @s run function rlk:boss/raiden/tm/glaive_fly2
execute if score @s rdTime matches 54 at @s rotated as @s run function rlk:boss/raiden/tm/glaive_land
execute if score @s rdTime matches 92 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:3500,b:0,c:0,d:0,e:14440000,f:0,tol:300,tell:12,dmg:20,life:23,ev:10,max:1,grp:0,dk:2,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 92 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/snd/bomb_tell
execute if score @s rdTime matches 104 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/bomb
execute if score @s rdTime matches 104 at @s rotated as @s run kill @e[tag=rlk_rd_tm_glaive]
execute if score @s rdTime matches 104 at @s rotated as @s run kill @e[tag=rlk_rd_tm_spot]
execute if score @s rdTime matches ..107 run return 0
execute if score @s rdTime matches 108 at @s rotated as @s run function rlk:boss/raiden/finish
