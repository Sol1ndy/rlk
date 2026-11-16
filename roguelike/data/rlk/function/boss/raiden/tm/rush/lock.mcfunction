# @s = the boss, tick 13: lock the arrival 1.5 b short of the player (kept 20 b inside the arena), turn to it, the
# flash, the three barrage hazards, and the rush path (start S, delta D in mb) for tm/rush/step.
kill @e[tag=rlk_rd_tm_spot]
kill @e[tag=rlk_rd_tm_step]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @s feet positioned ^ ^ ^1.5 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_spot"]}
execute as @e[tag=rlk_rd_tm_spot,limit=1] at @s unless entity @e[tag=rlk_raiden_arena,distance=..20] at @e[tag=rlk_raiden_arena,limit=1] facing entity @s feet positioned ^ ^ ^20 run tp @s ~ ~ ~
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_rd_tm_spot,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute positioned ^ ^1.4 ^1 run function rlk:boss/raiden/fx/star
execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:7000,b:0,c:0,d:0,e:53290000,f:0,tol:300,tell:15,dmg:14,life:26,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:2,go:0,sp:0,snd:1,nd:1,jp:0,det:0,lf:0,fv:0}
execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:7000,b:0,c:0,d:0,e:53290000,f:0,tol:300,tell:21,dmg:14,life:32,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:1,go:0,sp:0,snd:1,nd:1,jp:0,det:0,lf:0,fv:0}
execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:7000,b:0,c:0,d:0,e:53290000,f:0,tol:300,tell:27,dmg:14,life:38,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:3,go:0,sp:0,snd:1,nd:1,jp:0,det:0,lf:0,fv:0}
execute store result score #rdTmSX rd run data get entity @s Pos[0] 1000
execute store result score #rdTmSZ rd run data get entity @s Pos[2] 1000
execute store result score #rdTmDX rd run data get entity @e[tag=rlk_rd_tm_spot,limit=1] Pos[0] 1000
execute store result score #rdTmDZ rd run data get entity @e[tag=rlk_rd_tm_spot,limit=1] Pos[2] 1000
scoreboard players operation #rdTmDX rd -= #rdTmSX rd
scoreboard players operation #rdTmDZ rd -= #rdTmSZ rd
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_step"]}
