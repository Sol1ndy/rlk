# Fallback candidates (b): allowed in the band (bag and last ignored).
scoreboard players set #bfC11 mb 0
execute if score #bfBand mb matches 1 run scoreboard players set #bfC11 mb 2
execute if score #bfBand mb matches 2 run scoreboard players set #bfC11 mb 1
scoreboard players set #bfC12 mb 0
execute if score #bfBand mb matches 2 run scoreboard players set #bfC12 mb 1
execute if score #bfBand mb matches 3 run scoreboard players set #bfC12 mb 2
scoreboard players set #bfC13 mb 0
execute if score #bfBand mb matches 1 run scoreboard players set #bfC13 mb 1
execute if score #bfBand mb matches 2 run scoreboard players set #bfC13 mb 2
scoreboard players set #bfC14 mb 0
execute if score #bfBand mb matches 2 run scoreboard players set #bfC14 mb 1
execute if score #bfBand mb matches 3 run scoreboard players set #bfC14 mb 1
scoreboard players set #bfCn mb 0
scoreboard players operation #bfCn mb += #bfC11 mb
scoreboard players operation #bfCn mb += #bfC12 mb
scoreboard players operation #bfCn mb += #bfC13 mb
scoreboard players operation #bfCn mb += #bfC14 mb
