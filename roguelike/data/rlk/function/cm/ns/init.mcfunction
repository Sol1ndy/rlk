# 졸개 준비 (@s): 무리 번호(c2G) · 첫 마리가 무리장(rlk_ns_lead). 무리 소환(g_ns) 밖이면 혼자서 새 무리. 절반은 골드 · 회복 구슬 없음
execute unless score #c2InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1
scoreboard players operation @s c2G = #c2PackC tmp
execute unless score #c2InPack tmp matches 1 run tag @s add rlk_ns_lead
execute if score #c2InPack tmp matches 1 unless score #c2PackLd tmp matches 1 run tag @s add rlk_ns_lead
execute if score #c2InPack tmp matches 1 run scoreboard players set #c2PackLd tmp 1
execute store result score @s cmCd run random value 10..24
execute store result score @s c2T run random value 1..5
execute store result score #c2r tmp run random value 0..1
execute if score #c2r tmp matches 1 run tag @s add rlk_c2lite
function rlk:cm/ns/rig/create
tag @e[tag=rlk_c2this] remove rlk_c2this
