# 칸 하나 (macro: i = 이 쪽 안의 순번 0~23, 위치 = 칸의 가운데). 목록의 (쪽 × 24 + i)번째
$scoreboard players set #pkIdx tmp $(i)
scoreboard players operation #k tmp = @s cxPage
scoreboard players operation #k tmp *= #c24 tmp
scoreboard players operation #k tmp += #pkIdx tmp
execute store result storage rlk:codex a.k int 1 run scoreboard players get #k tmp
function rlk:codex/cell2 with storage rlk:codex a
