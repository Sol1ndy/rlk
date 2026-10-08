# 조준한 칸(pkHI)의 아이템 id → rlk:codex t.id (없으면 t.id 없음)
scoreboard players operation #k tmp = @s cxPage
scoreboard players operation #k tmp *= #c24 tmp
scoreboard players operation #k tmp += @s pkHI
execute store result storage rlk:codex t.k int 1 run scoreboard players get #k tmp
data remove storage rlk:codex t.id
function rlk:codex/tip_get with storage rlk:codex t
