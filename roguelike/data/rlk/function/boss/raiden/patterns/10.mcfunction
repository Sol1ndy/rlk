execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/cast
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/gaze
execute if score @s rdTime matches 0 at @s rotated as @s run kill @e[tag=rlk_rd_sgeye]
execute if score @s rdTime matches 0 at @s rotated as @s run execute store result score #rdSgSide rd run random value 0..1
execute if score @s rdTime matches 0 at @s rotated as @s run execute if score #rdSgSide rd matches 0 positioned ^6 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_rd_sgeye","rlk_rd_sgpt","rlk_rd_sg","rlk_rd_tmp","rlk_raiden_aux","rlk_room"]}
execute if score @s rdTime matches 0 at @s rotated as @s run execute if score #rdSgSide rd matches 1 positioned ^-6 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_rd_sgeye","rlk_rd_sgpt","rlk_rd_sg","rlk_rd_tmp","rlk_raiden_aux","rlk_room"]}
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/sg/clamp_pt
execute if score @s rdTime matches 0 at @s rotated as @s run tag @e[tag=rlk_rd_sgeye] remove rlk_rd_sgpt
execute if score @s rdTime matches 4 at @s rotated as @s run execute at @e[tag=rlk_rd_sgeye,limit=1] run function rlk:boss/raiden/fx/eye_spawn
execute if score @s rdTime matches 8 at @s rotated as @s run execute at @e[tag=rlk_rd_sgeye,limit=1] run function rlk:boss/raiden/object/create {kind:1,model:"prop/eye_orb",hp:6,id:10,y:1.0}
execute if score @s rdTime matches 8 at @s rotated as @s run execute at @e[tag=rlk_rd_sgeye,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:5000,b:0,c:0,d:0,e:28090000,f:0,tol:300,tell:140,dmg:30,life:151,ev:10,max:1,grp:0,dk:2,dl:20,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 8 at @s rotated as @s run function rlk:boss/raiden/sg/eye_hud
execute if score @s rdTime matches 28 at @s rotated as @s run execute if entity @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] run function rlk:boss/raiden/sg/eye_hud
execute if score @s rdTime matches 48 at @s rotated as @s run execute if entity @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] run function rlk:boss/raiden/sg/eye_hud
execute if score @s rdTime matches 68 at @s rotated as @s run execute if entity @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] run function rlk:boss/raiden/sg/eye_hud
execute if score @s rdTime matches 88 at @s rotated as @s run execute if entity @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] run function rlk:boss/raiden/sg/eye_hud
execute if score @s rdTime matches 108 at @s rotated as @s run execute if entity @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] run function rlk:boss/raiden/sg/eye_hud
execute if score @s rdTime matches 128 at @s rotated as @s run execute if entity @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] run function rlk:boss/raiden/sg/eye_hud
execute if score @s rdTime matches 122 at @s rotated as @s run execute as @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] at @s run function rlk:boss/raiden/fx/eye_glow {r:5,life:26}
execute if score @s rdTime matches 148 at @s rotated as @s run execute as @e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1] at @s run function rlk:boss/raiden/fx/eye_blast
execute if score @s rdTime matches 148 at @s rotated as @s run execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0
execute if score @s rdTime matches 148 at @s rotated as @s run function rlk:boss/raiden/object/clear
execute if score @s rdTime matches 150 at @s rotated as @s run function rlk:boss/raiden/finish
