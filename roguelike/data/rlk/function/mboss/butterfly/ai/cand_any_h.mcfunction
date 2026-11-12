# Fallback candidates (h): allowed in the band (bag and last ignored).
scoreboard players set #bfC1 mb 0
execute if score #bfBand mb matches 1 run scoreboard players set #bfC1 mb 2
execute if score #bfBand mb matches 2 run scoreboard players set #bfC1 mb 1
scoreboard players set #bfC2 mb 0
execute if score #bfBand mb matches 1 run scoreboard players set #bfC2 mb 1
execute if score #bfBand mb matches 2 run scoreboard players set #bfC2 mb 1
scoreboard players set #bfC3 mb 0
execute if score #bfBand mb matches 2 run scoreboard players set #bfC3 mb 1
execute if score #bfBand mb matches 3 run scoreboard players set #bfC3 mb 2
scoreboard players set #bfC4 mb 0
execute if score #bfBand mb matches 3 run scoreboard players set #bfC4 mb 2
execute if score #bfBand mb matches 2 run scoreboard players set #bfC4 mb 1
scoreboard players set #bfCn mb 0
scoreboard players operation #bfCn mb += #bfC1 mb
scoreboard players operation #bfCn mb += #bfC2 mb
scoreboard players operation #bfCn mb += #bfC3 mb
scoreboard players operation #bfCn mb += #bfC4 mb
