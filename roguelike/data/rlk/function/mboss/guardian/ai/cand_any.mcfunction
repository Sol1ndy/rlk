# Fallback candidates: allowed in the band and distance (bag and last ignored).
scoreboard players set #gdC1 mb 0
execute if score #gdBand mb matches 1 run scoreboard players set #gdC1 mb 2
execute if score #gdBand mb matches 2 run scoreboard players set #gdC1 mb 1
scoreboard players set #gdC2 mb 0
execute if score #gdBand mb matches 2 run scoreboard players set #gdC2 mb 1
execute if score #gdBand mb matches 3 run scoreboard players set #gdC2 mb 1
scoreboard players set #gdC3 mb 0
execute if score #gdBand mb matches 1 run scoreboard players set #gdC3 mb 2
scoreboard players set #gdC4 mb 0
execute if score #gdBand mb matches 1 run scoreboard players set #gdC4 mb 1
execute if score #gdBand mb matches 2 run scoreboard players set #gdC4 mb 1
execute if score #gdBand mb matches 3 run scoreboard players set #gdC4 mb 3
scoreboard players set #gdC5 mb 0
execute if score #gdBand mb matches 3 run scoreboard players set #gdC5 mb 3
scoreboard players set #gdCn mb 0
scoreboard players operation #gdCn mb += #gdC1 mb
scoreboard players operation #gdCn mb += #gdC2 mb
scoreboard players operation #gdCn mb += #gdC3 mb
scoreboard players operation #gdCn mb += #gdC4 mb
scoreboard players operation #gdCn mb += #gdC5 mb
