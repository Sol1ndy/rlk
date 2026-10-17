# Fallback candidates: allowed in the band (bag and last ignored).
scoreboard players set #gdC1 mb 0
execute if score #gdBand mb matches 1 run scoreboard players set #gdC1 mb 1
execute if score #gdBand mb matches 2 run scoreboard players set #gdC1 mb 1
scoreboard players set #gdC2 mb 0
execute if score #gdBand mb matches 2 run scoreboard players set #gdC2 mb 1
execute if score #gdBand mb matches 3 run scoreboard players set #gdC2 mb 1
scoreboard players set #gdC3 mb 0
execute if score #gdBand mb matches 1 run scoreboard players set #gdC3 mb 1
scoreboard players set #gdC4 mb 0
execute if score #gdBand mb matches 3 run scoreboard players set #gdC4 mb 1
scoreboard players set #gdC5 mb 0
execute if score #gdBand mb matches 3 run scoreboard players set #gdC5 mb 1
scoreboard players set #gdCn mb 0
execute if score #gdC1 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC2 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC3 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC4 mb matches 1 run scoreboard players add #gdCn mb 1
execute if score #gdC5 mb matches 1 run scoreboard players add #gdCn mb 1
