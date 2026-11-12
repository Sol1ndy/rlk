execute unless score #c3InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1
scoreboard players operation @s c2G = #c2PackC tmp
scoreboard players set @s c2R 0
scoreboard players set @s c3N 1
execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c2R = #c3Slot tmp
execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c3N = #c3Size tmp
execute if score #c3InPack tmp matches 1 run scoreboard players add #c3Slot tmp 1
execute store result score @s cmCd run random value 30..60
execute store result score @s c2T run random value 1..3
function rlk:cm/em/rig/create
tag @e[tag=rlk_c3this] remove rlk_c3this
