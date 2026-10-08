scoreboard players remove #tries tmp 1
execute store result score #len tmp run data get storage rlk:pick cand
# 후보 없으면 포기(무한루프 방지)
execute unless score #len tmp matches 1.. run scoreboard players set #pok tmp 1
# 랜덤 인덱스 = rand % len
execute if score #len tmp matches 1.. store result score #idx tmp run random value 0..1000000
execute if score #len tmp matches 1.. run scoreboard players operation #idx tmp %= #len tmp
execute if score #len tmp matches 1.. store result storage rlk:pick idx int 1 run scoreboard players get #idx tmp
execute if score #len tmp matches 1.. run function rlk:items/pick_get with storage rlk:pick
scoreboard players set #dup tmp 0
execute if data storage rlk:pick cid run function rlk:items/pick_dup with storage rlk:pick
# 소지 기반 제외(변신 상위형 보유 시 하위형 제외 등)
scoreboard players set #excl tmp 0
execute if data storage rlk:pick cid run function rlk:items/pick_excl
execute if score #dup tmp matches 0 if score #excl tmp matches 0 if data storage rlk:pick cid run function rlk:items/pick_accept
function rlk:items/pick_loop
