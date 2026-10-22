# 상점 노드의 등급 굴리기(rlk:shop nodewt 누적 %: 일반 · 레어 · 유니크, 나머지 레전더리) → 아이템 하나 → rlk:pick pid
data remove storage rlk:pick pid
execute store result score #rr tmp run random value 1..100
execute store result score #t1 tmp run data get storage rlk:shop nodewt.t1
execute store result score #t2 tmp run data get storage rlk:shop nodewt.t2
execute store result score #t3 tmp run data get storage rlk:shop nodewt.t3
scoreboard players set #g tmp 3
execute if score #rr tmp <= #t3 tmp run scoreboard players set #g tmp 2
execute if score #rr tmp <= #t2 tmp run scoreboard players set #g tmp 1
execute if score #rr tmp <= #t1 tmp run scoreboard players set #g tmp 0
function rlk:items/pick_item
# 그 등급에 남은 아이템이 없으면 다른 등급에서
execute unless data storage rlk:pick pid run scoreboard players set #g tmp 1
execute unless data storage rlk:pick pid run function rlk:items/pick_item
execute unless data storage rlk:pick pid run scoreboard players set #g tmp 0
execute unless data storage rlk:pick pid run function rlk:items/pick_item
execute unless data storage rlk:pick pid run scoreboard players set #g tmp 2
execute unless data storage rlk:pick pid run function rlk:items/pick_item
execute unless data storage rlk:pick pid run scoreboard players set #g tmp 3
execute unless data storage rlk:pick pid run function rlk:items/pick_item
