# Positioned at F1 / F2 1 t after its burst: the hail field (N6) r 4.0 / 100 t (never stacks Cryo); the
# hail keeps falling in it (one ambience chain for every live 45 hail field, every 8 t).
data modify storage rlk:mboss az.nf set value {fam:2,r:40,len:0,w:0,life:100,dmg:13,sh:0,area:50,rule:0,yaw:-999}
execute store result storage rlk:mboss az.nf.el int 1 run scoreboard players get #azET mb
function rlk:boss/azhdaha/fld/new
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p45h
function rlk:boss/azhdaha/fx/p/hail {r:40}
function rlk:boss/azhdaha/fx/snd/hail
execute unless score #aq45H mb matches 1 run function rlk:boss/azhdaha/p/icespike/hail_go
