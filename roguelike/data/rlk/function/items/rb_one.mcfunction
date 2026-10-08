data modify storage rlk:rb cur set from storage rlk:rb ids[0]
# 상자 제외 아이템이면 버킷에 안 넣음
scoreboard players set #ex tmp 0
function rlk:items/rb_chk with storage rlk:rb
execute if score #ex tmp matches 0 run function rlk:items/rb_bucket with storage rlk:rb
data remove storage rlk:rb ids[0]
function rlk:items/rb_loop
