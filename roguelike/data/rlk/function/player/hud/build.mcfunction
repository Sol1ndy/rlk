# 게이지 조립 (@s = 플레이어) → storage rlk:hud line (칸 목록, 칸 수 = #dashMax)
scoreboard players operation @s hudKey = #hk tmp
data modify storage rlk:hud line set value []
execute store result storage rlk:hud n int 1 run scoreboard players get #hn tmp
scoreboard players set #hi tmp 0
function rlk:player/hud/build_slot
