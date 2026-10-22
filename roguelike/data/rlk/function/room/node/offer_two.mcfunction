# 둘째 노드: 이번 선택지들에 나온 노드(첫 노드 포함)와 다른 것
scoreboard players set #noRoot tmp 1
function rlk:room/node/draw_fresh
scoreboard players set #noRoot tmp 0
execute if score #nk tmp matches ..0 run return 0
function rlk:room/node/take
