# 노드 맵: rlk:room next 의 노드마다 서로 다른 중간 구역(1 ~ n-2번째) 하나를 그 종류로
execute store result score #n tmp run data get storage rlk:room cur.n
scoreboard players remove #n tmp 2
data modify storage rlk:room mids set value []
scoreboard players set #mi tmp 1
function rlk:room/node/mids_loop
data modify storage rlk:room pq set from storage rlk:room next
function rlk:room/node/place_loop
