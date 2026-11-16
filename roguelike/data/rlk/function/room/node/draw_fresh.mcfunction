# used(이번 선택지들에 나온 노드) + seen(이번 챕터에 고른 노드)을 빼고 뽑기 → #nk. 후보가 없으면 seen 은 허용하고 다시
data modify storage rlk:room excl set from storage rlk:room used
scoreboard players set #nSeen tmp 1
function rlk:room/node/draw
execute if score #nk tmp matches 1.. run return 0
scoreboard players set #nSeen tmp 0
function rlk:room/node/draw
