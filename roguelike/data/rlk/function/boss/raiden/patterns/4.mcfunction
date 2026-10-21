execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/cast
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/eyes
execute if score @s rdTime matches 6 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-10 ~ ~-6 run function rlk:boss/raiden/fx/eye_spawn
execute if score @s rdTime matches 6 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~10 ~ ~-6 run function rlk:boss/raiden/fx/eye_spawn
execute if score @s rdTime matches 6 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~0 ~ ~11 run function rlk:boss/raiden/fx/eye_spawn
execute if score @s rdTime matches 10 at @s rotated as @s run scoreboard players add #rdGrpSerial rd 1
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-10 ~ ~-6 run function rlk:boss/raiden/object/create {kind:1,model:"prop/eye_orb",hp:4,id:1,y:1.7}
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-10 ~ ~-6 run function rlk:boss/raiden/hazard/new {k:1,a:12000,b:0,c:0,d:0,e:151290000,f:0,tol:300,tell:130,dmg:34,life:141,ev:10,max:1,grp:1,dk:1,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~10 ~ ~-6 run function rlk:boss/raiden/object/create {kind:1,model:"prop/eye_orb",hp:4,id:2,y:1.7}
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~10 ~ ~-6 run function rlk:boss/raiden/hazard/new {k:1,a:12000,b:0,c:0,d:0,e:151290000,f:0,tol:300,tell:130,dmg:34,life:141,ev:10,max:1,grp:1,dk:1,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~0 ~ ~11 run function rlk:boss/raiden/object/create {kind:1,model:"prop/eye_orb",hp:4,id:3,y:1.7}
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~0 ~ ~11 run function rlk:boss/raiden/hazard/new {k:1,a:12000,b:0,c:0,d:0,e:151290000,f:0,tol:300,tell:130,dmg:34,life:141,ev:10,max:1,grp:1,dk:1,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 114 at @s rotated as @s run execute as @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=1..3}] at @s run function rlk:boss/raiden/fx/eye_glow {r:12,life:26}
execute if score @s rdTime matches 140 at @s rotated as @s run execute as @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=1..3}] at @s run function rlk:boss/raiden/fx/eye_blast
execute if score @s rdTime matches 140 at @s rotated as @s run function rlk:boss/raiden/object/clear
execute if score @s rdTime matches 150 at @s rotated as @s run function rlk:boss/raiden/finish
