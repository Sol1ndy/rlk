# nw 의 항목마다: 조건이 맞고 excl 에 없으면 cand 에 넣고 가중치를 더한다
execute unless data storage rlk:room wq[0] run return 0
execute store result score #ck tmp run data get storage rlk:room wq[0].k
scoreboard players set #cok tmp 1
# 나무뿌리: 이번 판에 이미 기적을 받았으면 X
execute if score #ck tmp matches 8 if score #mirUsed room matches 1.. run scoreboard players set #cok tmp 0
# 나무뿌리: 지금 맵에 아직 쓰지 않은 나무뿌리가 있으면 다음 맵에는 안 낸다(둘 중 하나는 헛것이 됨)
execute if score #ck tmp matches 8 if entity @e[tag=rlk_zone,scores={zkind=8}] run scoreboard players set #cok tmp 0
# 나무뿌리: 둘째 노드로는 X (혼자만 나옴)
execute if score #ck tmp matches 8 if score #noRoot tmp matches 1 run scoreboard players set #cok tmp 0
# 보유 칸: 3챕터부터, 18칸 미만일 때만
execute if score #ck tmp matches 12 if score #chapter room matches ..2 run scoreboard players set #cok tmp 0
execute if score #ck tmp matches 12 if entity @a[tag=player,limit=1,scores={invCap=18..}] run scoreboard players set #cok tmp 0
# 중간보스: 1챕터의 첫 선택지(시작 아이템 하나뿐)에는 X, 뽑을 수 있는 중간보스가 없으면 X
execute if score #ck tmp matches 15 if score #chapter room matches ..1 if score #mapIdx room matches ..0 run scoreboard players set #cok tmp 0
execute if score #ck tmp matches 15 unless score #mbRoll mb matches 1.. run scoreboard players set #cok tmp 0
# 뺄 목록
data modify storage rlk:room xq set from storage rlk:room excl
execute if score #cok tmp matches 1 run function rlk:room/node/excl_loop
# 이번 챕터에 고른 노드 (#nSeen 1 일 때만)
execute if score #cok tmp matches 1 if score #nSeen tmp matches 1 run data modify storage rlk:room xq set from storage rlk:room seen
execute if score #cok tmp matches 1 if score #nSeen tmp matches 1 run function rlk:room/node/excl_loop
execute if score #cok tmp matches 1 run data modify storage rlk:room cand append from storage rlk:room wq[0]
execute if score #cok tmp matches 1 store result score #cw tmp run data get storage rlk:room wq[0].w
execute if score #cok tmp matches 1 run scoreboard players operation #wsum tmp += #cw tmp
data remove storage rlk:room wq[0]
function rlk:room/node/cand_loop
