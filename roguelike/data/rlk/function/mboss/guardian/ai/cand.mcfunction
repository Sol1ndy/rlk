# Candidates: in the bag, allowed in the current range band, not the last one.
scoreboard players set #gdC1 mb 0
execute if score #gdBag1 mb matches 1 if score #gdBand mb matches 1 unless score #gdLast mb matches 1 run scoreboard players set #gdC1 mb 1
execute if score #gdBag1 mb matches 1 if score #gdBand mb matches 2 unless score #gdLast mb matches 1 run scoreboard players set #gdC1 mb 1
scoreboard players set #gdC2 mb 0
execute if score #gdBag2 mb matches 1 if score #gdBand mb matches 2 unless score #gdLast mb matches 2 run scoreboard players set #gdC2 mb 1
execute if score #gdBag2 mb matches 1 if score #gdBand mb matches 3 unless score #gdLast mb matches 2 run scoreboard players set #gdC2 mb 1
scoreboard players set #gdC3 mb 0
execute if score #gdBag3 mb matches 1 if score #gdBand mb matches 1 unless score #gdLast mb matches 3 run scoreboard players set #gdC3 mb 1
scoreboard players set #gdC4 mb 0
execute if score #gdBag4 mb matches 1 if score #gdBand mb matches 3 unless score #gdLast mb matches 4 run scoreboard players set #gdC4 mb 1
scoreboard players set #gdC5 mb 0
execute if score #gdBag5 mb matches 1 if score #gdBand mb matches 3 unless score #gdLast mb matches 5 run scoreboard players set #gdC5 mb 1
scoreboard players set #gdCn mb 0
execute if score #gdC1 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC2 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC3 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC4 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC5 mb matches 1 run scoreboard players add #gdCn mb 1
