execute unless score #c3InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1
scoreboard players operation @s c2G = #c2PackC tmp
scoreboard players set @s c2R 0
scoreboard players set @s c3N 1
execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c2R = #c3Slot tmp
execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c3N = #c3Size tmp
execute if score #c3InPack tmp matches 1 run scoreboard players add #c3Slot tmp 1
# 땅속에서 시작(맞힐 수 없음). 무리는 같은 타이머(#c3SbT)로 함께 솟음. 넷 중 셋은 골드 · 회복 구슬 없음
function rlk:cm/sb/hide
execute store result score @s c2T run random value 20..50
execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c2T = #c3SbT tmp
scoreboard players set @s c2T2 -1
execute store result score #c3r tmp run random value 0..3
execute unless score #c3r tmp matches 0 run tag @s add rlk_c2lite
function rlk:cm/sb/rig/create
tag @e[tag=rlk_c3this] remove rlk_c3this
