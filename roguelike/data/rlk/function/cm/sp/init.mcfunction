# 창병 준비 (@s): 대열 번호(c2G) · 자리(c2R 0 왼쪽 1 가운데 2 오른쪽), 바라보는 방향 = 소환 방향
execute unless score #c2InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1
scoreboard players operation @s c2G = #c2PackC tmp
scoreboard players set @s c2R 1
execute if score #c2InPack tmp matches 1 run scoreboard players operation @s c2R = #c2Slot tmp
execute store result score @s cmYaw run data get entity @s Rotation[0] 100
execute store result score @s cmCd run random value 20..40
scoreboard players set @s c2T 4
function rlk:cm/sp/rig/create
tag @e[tag=rlk_c2this] remove rlk_c2this
