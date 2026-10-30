# 다음 맵 선택지 3개 (@s = 마지막 구역 표식, at @s). 선택지마다 노드 1개(가끔 2개)
# 선택지 k 의 노드 = rlk:room offers[k].nodes (구역 종류 목록). 오브젝트는 oact 9, oarg = k
data modify storage rlk:room offers set value [{nodes:[]},{nodes:[]},{nodes:[]}]
# 세 선택지에 같은 노드가 겹치지 않게 (used)
data modify storage rlk:room used set value []
execute unless data storage rlk:room seen run data modify storage rlk:room seen set value []
scoreboard players set #slot tmp 0
function rlk:room/node/offer_one
scoreboard players set #slot tmp 1
function rlk:room/node/offer_one
scoreboard players set #slot tmp 2
function rlk:room/node/offer_one
scoreboard players set #slot tmp 0
execute positioned ~-5 ~ ~ run function rlk:room/node/spawn
scoreboard players set #slot tmp 1
execute positioned ~ ~ ~ run function rlk:room/node/spawn
scoreboard players set #slot tmp 2
execute positioned ~5 ~ ~ run function rlk:room/node/spawn
