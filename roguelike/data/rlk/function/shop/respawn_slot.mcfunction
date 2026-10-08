# at = 슬롯 블록 코너. 이 슬롯의 진열품을 지우고 다시 추첨
function rlk:shop/kill_slot
particle minecraft:witch ~0.5 ~1.5 ~0.5 0.6 0.5 0.6 0.02 20
function rlk:shop/roll_pick
execute if data storage rlk:pick pid run function rlk:shop/place_item
