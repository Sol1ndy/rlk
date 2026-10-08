# 보유 아이템 1개를 다른 아이템으로 교체 (@s = 플레이어). macro: from, to. 예: {from:"sealed_sword",to:"sword_kirion"}
$execute if score @s devMode matches 1 run return run function rlk:items/order_replace_dev {from:"$(from)",to:"$(to)"}
# order 에서 from 1개 제거 → to 추가 → 재배치
$data modify storage rlk:pinv t1 set value "$(from)"
scoreboard players set #n1 tmp 1
data modify storage rlk:pinv sscan set from storage rlk:pinv order
data modify storage rlk:pinv order set value []
function rlk:items/order_strip_loop
$data modify storage rlk:pinv order append value "$(to)"
function rlk:player/inv/place_items
