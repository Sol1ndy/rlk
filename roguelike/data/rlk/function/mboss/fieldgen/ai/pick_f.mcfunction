# @s = body. Range-filtered, weighted shuffle bag of the field state, no immediate repeat:
# fzone melee/mid/far, frock melee/mid/far (melee <= 4.0 b, far >= 8.0 b).
function rlk:mboss/mv/dist
scoreboard players operation #fgDist mb = #mbDist mb
scoreboard players set #fgBand mb 2
execute if score #fgDist mb matches ..40 run scoreboard players set #fgBand mb 1
execute if score #fgDist mb matches 80.. run scoreboard players set #fgBand mb 3
function rlk:mboss/fieldgen/ai/cand_f
execute if score #fgCn mb matches 0 run function rlk:mboss/fieldgen/ai/refill_f
execute if score #fgCn mb matches 0 run function rlk:mboss/fieldgen/ai/cand_f
execute if score #fgCn mb matches 0 run function rlk:mboss/fieldgen/ai/cand_any_f
execute if score #fgCn mb matches 0 run scoreboard players set #fgC11 mb 1
execute if score #fgCn mb matches 0 run scoreboard players set #fgCn mb 1
execute store result score #fgR mb run random value 0..999
scoreboard players operation #fgR mb %= #fgCn mb
function rlk:mboss/fieldgen/ai/draw_f
execute if score #fgPick mb matches 0 run scoreboard players set #fgPick mb 11
scoreboard players operation #fgLast mb = #fgPick mb
function rlk:mboss/fieldgen/ai/go
