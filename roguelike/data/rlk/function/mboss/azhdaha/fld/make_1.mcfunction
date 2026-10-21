# Field slot 1 (positioned at the field, rotated = its line yaw).
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld1]
execute store result score #azNfL mb run data get storage rlk:mboss az.nf.life
execute store result score #hzAct mb run data get storage rlk:mboss az.nf.life
scoreboard players set #hzRearm mb 10
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzSfx mb 0
execute store result score #hzEl mb run data get storage rlk:mboss az.nf.el
scoreboard players set #hzNR mb 1
# the family's volley group (one tick per 10 t however many fields of that family overlap)
execute if score #azNfF mb matches 1 unless score #azFG1 mb matches 1.. run function rlk:mboss/grp_new
execute if score #azNfF mb matches 1 unless score #azFG1 mb matches 1.. run scoreboard players operation #azFG1 mb = #mbGrp mb
execute if score #azNfF mb matches 1 run scoreboard players operation #hzGrp mb = #azFG1 mb
execute if score #azNfF mb matches 2 unless score #azFG2 mb matches 1.. run function rlk:mboss/grp_new
execute if score #azNfF mb matches 2 unless score #azFG2 mb matches 1.. run scoreboard players operation #azFG2 mb = #mbGrp mb
execute if score #azNfF mb matches 2 run scoreboard players operation #hzGrp mb = #azFG2 mb
execute if score #azNfF mb matches 3 unless score #azFG3 mb matches 1.. run function rlk:mboss/grp_new
execute if score #azNfF mb matches 3 unless score #azFG3 mb matches 1.. run scoreboard players operation #azFG3 mb = #mbGrp mb
execute if score #azNfF mb matches 3 run scoreboard players operation #hzGrp mb = #azFG3 mb
execute store result storage rlk:mboss az.nf.tell int 1 run scoreboard players set #azX mb 1
execute if data storage rlk:mboss az.nf{sh:0} run function rlk:mboss/hz/disc with storage rlk:mboss az.nf
execute if data storage rlk:mboss az.nf{sh:1} run function rlk:mboss/azhdaha/fld/line with storage rlk:mboss az.nf
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_fld1
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_fld
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_fld1] azF 1
scoreboard players operation #azF1 mb = #azNfF mb
scoreboard players operation #azFE1 mb = #azClk mb
scoreboard players operation #azFE1 mb += #azNfL mb
scoreboard players operation #azFT1 mb = #azClk mb
scoreboard players operation #azFB1 mb = #azNfL mb
scoreboard players add #azFSeq mb 1
scoreboard players operation #azFS1 mb = #azFSeq mb
scoreboard players operation #azFA1 mb = #azNfA mb
scoreboard players operation #azFldA mb += #azNfA mb
scoreboard players add #azFldN mb 1
data modify storage rlk:mboss az.f1 set from storage rlk:mboss az.nf
execute store result storage rlk:mboss az.f1.x double 0.001 run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_fld1,limit=1] Pos[0] 1000
execute store result storage rlk:mboss az.f1.y double 0.001 run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_fld1,limit=1] Pos[1] 1000
execute store result storage rlk:mboss az.f1.z double 0.001 run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_fld1,limit=1] Pos[2] 1000
execute store result storage rlk:mboss az.f1.ry int 1 run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_fld1,limit=1] Rotation[0]
data modify storage rlk:mboss az.f1.id set value 1
function rlk:mboss/azhdaha/fld/draw_1
