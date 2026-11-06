# order 순서대로 inventory.9~ 의 invCap 칸에 배치 (틀린 칸만 수정) + 남는 칸 비움 + 잠긴 칸(invCap 밖, ~inventory.26)은 방벽 (@s = 플레이어)
execute unless score @s invCap matches 9..18 run scoreboard players set @s invCap 9
scoreboard players set #siMax tmp 8
scoreboard players operation #siMax tmp += @s invCap
scoreboard players set #si tmp 9
data modify storage rlk:pinv q set from storage rlk:pinv order
function rlk:player/inv/place_items_loop
function rlk:player/inv/place_items_clear
function rlk:player/inv/place_lock
