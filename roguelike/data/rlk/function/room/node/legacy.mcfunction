# 예전 판의 맵 선택지(oact 7, oarg = 맵 종류 1~7)를 노드 맵으로 바꿔 진행 (@s = 오브젝트 표식)
data modify storage rlk:room next set value []
execute if score @s oarg matches 1 run data modify storage rlk:room next set value [3]
execute if score @s oarg matches 2 run data modify storage rlk:room next set value [4,3]
execute if score @s oarg matches 3 run data modify storage rlk:room next set value [5]
execute if score @s oarg matches 4 run data modify storage rlk:room next set value [10]
execute if score @s oarg matches 5 run data modify storage rlk:room next set value [8]
execute if score @s oarg matches 6 run data modify storage rlk:room next set value [3]
execute if score @s oarg matches 7 run data modify storage rlk:room next set value [7]
function rlk:room/node/validate
scoreboard players set #mapType room 1
function rlk:run/next_map
