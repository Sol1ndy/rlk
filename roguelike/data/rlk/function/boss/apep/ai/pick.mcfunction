# @s = body: the weighted pick in the sampled column.
function rlk:boss/apep/ai/cand
execute if score #apCn mb matches 0 run return run function rlk:boss/apep/ai/fallback
execute store result score #apR mb run random value 0..9999
scoreboard players operation #apR mb %= #apCn mb
function rlk:boss/apep/ai/draw
execute if score #apPick mb matches 0 run return run function rlk:boss/apep/ai/fallback
scoreboard players set #apArg mb 0
function rlk:boss/apep/ai/go
