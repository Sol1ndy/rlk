# 칸 표식: 진입 판정 범위(좌표 × 100). 그 구역에 들어가면 지워진다
$summon minecraft:marker $(x0).0 201 $(z0).0 {Tags:["rlk_room","rlk_zcell","rlk_new"]}
scoreboard players operation @e[tag=rlk_new,limit=1] zid = #zid tmp
execute store result score @e[tag=rlk_new,limit=1] ex0 run data get storage rlk:room ce.ex0
execute store result score @e[tag=rlk_new,limit=1] ex1 run data get storage rlk:room ce.ex1
execute store result score @e[tag=rlk_new,limit=1] ez0 run data get storage rlk:room ce.ez0
execute store result score @e[tag=rlk_new,limit=1] ez1 run data get storage rlk:room ce.ez1
tag @e[tag=rlk_new] remove rlk_new
