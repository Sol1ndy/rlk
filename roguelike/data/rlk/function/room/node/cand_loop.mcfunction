# nw 의 항목마다: 조건이 맞고 excl 에 없으면 cand 에 넣고 가중치를 더한다
execute unless data storage rlk:room wq[0] run return 0
execute store result score #ck tmp run data get storage rlk:room wq[0].k
scoreboard players set #cok tmp 1
# 나무뿌리: 이번 판에 이미 기적을 받았으면 X
execute if score #ck tmp matches 8 if score #mirUsed room matches 1.. run scoreboard players set #cok tmp 0
# 보유 칸: 3챕터부터, 18칸 미만일 때만
execute if score #ck tmp matches 12 if score #chapter room matches ..2 run scoreboard players set #cok tmp 0
execute if score #ck tmp matches 12 if entity @a[tag=player,limit=1,scores={invCap=18..}] run scoreboard players set #cok tmp 0
# 뺄 목록
data modify storage rlk:room xq set from storage rlk:room excl
execute if score #cok tmp matches 1 run function rlk:room/node/excl_loop
execute if score #cok tmp matches 1 run data modify storage rlk:room cand append from storage rlk:room wq[0]
execute if score #cok tmp matches 1 store result score #cw tmp run data get storage rlk:room wq[0].w
execute if score #cok tmp matches 1 run scoreboard players operation #wsum tmp += #cw tmp
data remove storage rlk:room wq[0]
function rlk:room/node/cand_loop
