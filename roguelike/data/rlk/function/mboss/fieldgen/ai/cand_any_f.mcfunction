# Fallback candidates (f): allowed in the band (bag and last ignored).
scoreboard players set #fgC11 mb 0
execute if score #fgBand mb matches 1 unless score #fgLast mb matches 11 run scoreboard players set #fgC11 mb 1
execute if score #fgBand mb matches 2 unless score #fgLast mb matches 11 run scoreboard players set #fgC11 mb 1
execute if score #fgBand mb matches 3 unless score #fgLast mb matches 11 run scoreboard players set #fgC11 mb 1
scoreboard players set #fgC12 mb 0
execute if score #fgBand mb matches 1 unless score #fgLast mb matches 12 run scoreboard players set #fgC12 mb 1
execute if score #fgBand mb matches 2 unless score #fgLast mb matches 12 run scoreboard players set #fgC12 mb 1
execute if score #fgBand mb matches 3 unless score #fgLast mb matches 12 run scoreboard players set #fgC12 mb 1
scoreboard players set #fgCn mb 0
scoreboard players operation #fgCn mb += #fgC11 mb
scoreboard players operation #fgCn mb += #fgC12 mb
