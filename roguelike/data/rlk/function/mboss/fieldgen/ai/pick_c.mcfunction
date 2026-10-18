# @s = body. Range-filtered, weighted shuffle bag of the cruise state, no immediate repeat:
# bomb mid/farx2, slam meleex2/mid, laser meleex2/midx2, missile farx3, burst meleex2/mid, rock midx2/far (melee <= 4.0 b, far >= 8.0 b).
function rlk:mboss/mv/dist
scoreboard players operation #fgDist mb = #mbDist mb
scoreboard players set #fgBand mb 2
execute if score #fgDist mb matches ..40 run scoreboard players set #fgBand mb 1
execute if score #fgDist mb matches 80.. run scoreboard players set #fgBand mb 3
function rlk:mboss/fieldgen/ai/cand_c
execute if score #fgCn mb matches 0 run function rlk:mboss/fieldgen/ai/refill_c
execute if score #fgCn mb matches 0 run function rlk:mboss/fieldgen/ai/cand_c
execute if score #fgCn mb matches 0 run function rlk:mboss/fieldgen/ai/cand_any_c
execute if score #fgCn mb matches 0 run scoreboard players set #fgC1 mb 1
execute if score #fgCn mb matches 0 run scoreboard players set #fgCn mb 1
execute store result score #fgR mb run random value 0..999
scoreboard players operation #fgR mb %= #fgCn mb
function rlk:mboss/fieldgen/ai/draw_c
execute if score #fgPick mb matches 0 run scoreboard players set #fgPick mb 1
scoreboard players operation #fgLast mb = #fgPick mb
function rlk:mboss/fieldgen/ai/go
