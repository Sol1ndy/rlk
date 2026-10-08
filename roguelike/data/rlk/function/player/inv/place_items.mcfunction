# order 순서대로 inventory.9~17 에 배치 (틀린 칸만 수정) + 남는 칸 비움 (@s = 플레이어)
scoreboard players set #si tmp 9
data modify storage rlk:pinv q set from storage rlk:pinv order
function rlk:player/inv/place_items_loop
function rlk:player/inv/place_items_clear
