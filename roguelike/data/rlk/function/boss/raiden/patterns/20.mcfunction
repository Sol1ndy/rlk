# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/foolish
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdTmCD 300
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run execute positioned ~ ~2.6 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 8 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_spin_throw
execute if score @s rdTime matches 8 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:2,a:2000,b:7000,c:0,d:-1000,e:53290000,f:2890000,tol:300,tell:12,dmg:18,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:6,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches ..19 run return 0
execute if score @s rdTime matches 20 at @s rotated as @s run function rlk:boss/raiden/fx/snd/glaive_sweep
execute if score @s rdTime matches 26 at @s rotated as @s run kill @e[tag=rlk_rd_tm_spot]
execute if score @s rdTime matches 26 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_spot"]}
execute if score @s rdTime matches 26 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 26 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 26 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:3000,b:0,c:0,d:0,e:10890000,f:0,tol:300,tell:12,dmg:18,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 26 at @s rotated as @s run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.7 1.3 0.3
execute if score @s rdTime matches ..37 run return 0
execute if score @s rdTime matches 38 at @s rotated as @s run function rlk:boss/raiden/tm/glaive_land
execute if score @s rdTime matches 76 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:3500,b:0,c:0,d:0,e:14440000,f:0,tol:300,tell:12,dmg:20,life:23,ev:10,max:1,grp:0,dk:2,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 76 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/snd/bomb_tell
execute if score @s rdTime matches 88 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/bomb
execute if score @s rdTime matches 88 at @s rotated as @s run kill @e[tag=rlk_rd_tm_glaive]
execute if score @s rdTime matches 88 at @s rotated as @s run kill @e[tag=rlk_rd_tm_spot]
execute if score @s rdTime matches ..91 run return 0
execute if score @s rdTime matches 92 at @s rotated as @s run function rlk:boss/raiden/finish
