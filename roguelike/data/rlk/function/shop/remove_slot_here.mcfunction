# at = 슬롯 블록 코너. 엔티티·블록·저장 슬롯 모두 제거
function rlk:shop/kill_slot
setblock ~ ~1 ~ minecraft:air
setblock ~ ~ ~ minecraft:air
particle minecraft:cloud ~0.5 ~1 ~0.5 0.4 0.4 0.4 0.02 20
function rlk:shop/slot_forget
