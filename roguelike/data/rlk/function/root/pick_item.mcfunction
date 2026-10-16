# macro: e = 각인 id → rlk:room gid = 그 각인이 달린 아이템(rlk:engravings byeng.<id>) 중 무작위 하나 (없으면 gid 없음)
# 아직 가지지 않았고 다른 카드에 나오지 않은 아이템이 있으면 그중에서
data remove storage rlk:room gid
$data modify storage rlk:room gq set from storage rlk:engravings byeng.$(e)
data modify storage rlk:room gq2 set value []
data modify storage rlk:room gs set from storage rlk:room gq
function rlk:root/give_filter
execute if data storage rlk:room gq2[0] run data modify storage rlk:room gq set from storage rlk:room gq2
execute store result score #gl tmp run data get storage rlk:room gq
execute if score #gl tmp matches ..0 run return 0
execute store result score #r tmp run random value 0..9999
scoreboard players operation #r tmp %= #gl tmp
execute store result storage rlk:room a.r int 1 run scoreboard players get #r tmp
function rlk:root/give2 with storage rlk:room a
