# Candidates (c): in the bag, allowed in the current range band, not the last one.
# #fgC<id> = its draw weight in this band (0 = no candidate).
scoreboard players set #fgC1 mb 0
execute if score #fgBag1 mb matches 1 if score #fgBand mb matches 1 unless score #fgLast mb matches 1 run scoreboard players set #fgC1 mb 1
execute if score #fgBag1 mb matches 1 if score #fgBand mb matches 2 unless score #fgLast mb matches 1 run scoreboard players set #fgC1 mb 1
execute if score #fgBag1 mb matches 1 if score #fgBand mb matches 3 unless score #fgLast mb matches 1 run scoreboard players set #fgC1 mb 2
scoreboard players set #fgC2 mb 0
execute if score #fgBag2 mb matches 1 if score #fgBand mb matches 1 unless score #fgLast mb matches 2 run scoreboard players set #fgC2 mb 2
execute if score #fgBag2 mb matches 1 if score #fgBand mb matches 2 unless score #fgLast mb matches 2 run scoreboard players set #fgC2 mb 1
scoreboard players set #fgC3 mb 0
execute if score #fgBag3 mb matches 1 if score #fgBand mb matches 2 unless score #fgLast mb matches 3 run scoreboard players set #fgC3 mb 2
scoreboard players set #fgC4 mb 0
execute if score #fgBag4 mb matches 1 if score #fgBand mb matches 3 unless score #fgLast mb matches 4 run scoreboard players set #fgC4 mb 3
scoreboard players set #fgC5 mb 0
execute if score #fgBag5 mb matches 1 if score #fgBand mb matches 2 unless score #fgLast mb matches 5 run scoreboard players set #fgC5 mb 1
scoreboard players set #fgC6 mb 0
execute if score #fgBag6 mb matches 1 if score #fgBand mb matches 1 unless score #fgLast mb matches 6 run scoreboard players set #fgC6 mb 1
execute if score #fgBag6 mb matches 1 if score #fgBand mb matches 2 unless score #fgLast mb matches 6 run scoreboard players set #fgC6 mb 2
execute if score #fgBag6 mb matches 1 if score #fgBand mb matches 3 unless score #fgLast mb matches 6 run scoreboard players set #fgC6 mb 1
scoreboard players set #fgCn mb 0
scoreboard players operation #fgCn mb += #fgC1 mb
scoreboard players operation #fgCn mb += #fgC2 mb
scoreboard players operation #fgCn mb += #fgC3 mb
scoreboard players operation #fgCn mb += #fgC4 mb
scoreboard players operation #fgCn mb += #fgC5 mb
scoreboard players operation #fgCn mb += #fgC6 mb
