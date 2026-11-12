execute unless score #c3InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1
scoreboard players operation @s c2G = #c2PackC tmp
scoreboard players set @s c2R 0
scoreboard players set @s c3N 1
execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c2R = #c3Slot tmp
execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c3N = #c3Size tmp
execute if score #c3InPack tmp matches 1 run scoreboard players add #c3Slot tmp 1
# 첫 마리가 무리장(rlk_fu_lead). 절반은 골드 · 회복 구슬 없음
execute unless score #c3InPack tmp matches 1 run tag @s add rlk_fu_lead
execute if score #c3InPack tmp matches 1 unless score #c3PackLd tmp matches 1 run tag @s add rlk_fu_lead
execute if score #c3InPack tmp matches 1 run scoreboard players set #c3PackLd tmp 1
execute store result score @s cmCd run random value 12..36
execute store result score @s c2T run random value 1..4
execute store result score #c3r tmp run random value 0..1
execute if score #c3r tmp matches 1 run tag @s add rlk_c2lite
function rlk:cm/fu/rig/create
tag @e[tag=rlk_c3this] remove rlk_c3this
