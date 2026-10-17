# Candidates: in the bag, allowed in the current range band (and distance), not the last one.
# #gdC<id> = its draw weight in this band (0 = no candidate).
scoreboard players set #gdC1 mb 0
execute if score #gdBag1 mb matches 1 if score #gdBand mb matches 1 unless score #gdLast mb matches 1 run scoreboard players set #gdC1 mb 1
execute if score #gdBag1 mb matches 1 if score #gdBand mb matches 2 unless score #gdLast mb matches 1 run scoreboard players set #gdC1 mb 1
scoreboard players set #gdC2 mb 0
execute if score #gdBag2 mb matches 1 if score #gdBand mb matches 2 unless score #gdLast mb matches 2 run scoreboard players set #gdC2 mb 1
execute if score #gdBag2 mb matches 1 if score #gdBand mb matches 3 unless score #gdLast mb matches 2 run scoreboard players set #gdC2 mb 1
scoreboard players set #gdC3 mb 0
execute if score #gdBag3 mb matches 1 if score #gdBand mb matches 1 unless score #gdLast mb matches 3 run scoreboard players set #gdC3 mb 1
scoreboard players set #gdC4 mb 0
execute if score #gdBag4 mb matches 1 if score #gdBand mb matches 2 if score #gdDist mb matches 50.. unless score #gdLast mb matches 4 run scoreboard players set #gdC4 mb 1
execute if score #gdBag4 mb matches 1 if score #gdBand mb matches 3 if score #gdDist mb matches 50.. unless score #gdLast mb matches 4 run scoreboard players set #gdC4 mb 3
scoreboard players set #gdC5 mb 0
execute if score #gdBag5 mb matches 1 if score #gdBand mb matches 3 unless score #gdLast mb matches 5 run scoreboard players set #gdC5 mb 3
scoreboard players set #gdCn mb 0
scoreboard players operation #gdCn mb += #gdC1 mb
scoreboard players operation #gdCn mb += #gdC2 mb
scoreboard players operation #gdCn mb += #gdC3 mb
scoreboard players operation #gdCn mb += #gdC4 mb
scoreboard players operation #gdCn mb += #gdC5 mb
