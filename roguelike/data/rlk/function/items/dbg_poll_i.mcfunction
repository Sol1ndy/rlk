# @s = 플레이어, at @s. dbgDropI = 아이템 인덱스(1기준) → 드롭
scoreboard players operation #di tmp = @s dbgDropI
scoreboard players remove #di tmp 1
scoreboard players set @s dbgDropI 0
execute store result storage rlk:dbgt n int 1 run scoreboard players get #di tmp
function rlk:items/dbg_poll_i2 with storage rlk:dbgt
