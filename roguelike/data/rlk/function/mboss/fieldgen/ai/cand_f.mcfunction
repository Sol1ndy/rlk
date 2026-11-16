# Candidates (f): in the bag, allowed in the current range band, not the last one.
# #fgC<id> = its draw weight in this band (0 = no candidate).
scoreboard players set #fgC11 mb 0
execute if score #fgBag11 mb matches 1 if score #fgBand mb matches 1 unless score #fgLast mb matches 11 run scoreboard players set #fgC11 mb 1
execute if score #fgBag11 mb matches 1 if score #fgBand mb matches 2 unless score #fgLast mb matches 11 run scoreboard players set #fgC11 mb 1
execute if score #fgBag11 mb matches 1 if score #fgBand mb matches 3 unless score #fgLast mb matches 11 run scoreboard players set #fgC11 mb 1
scoreboard players set #fgC12 mb 0
execute if score #fgBag12 mb matches 1 if score #fgBand mb matches 1 unless score #fgLast mb matches 12 run scoreboard players set #fgC12 mb 1
execute if score #fgBag12 mb matches 1 if score #fgBand mb matches 2 unless score #fgLast mb matches 12 run scoreboard players set #fgC12 mb 1
execute if score #fgBag12 mb matches 1 if score #fgBand mb matches 3 unless score #fgLast mb matches 12 run scoreboard players set #fgC12 mb 1
scoreboard players set #fgCn mb 0
scoreboard players operation #fgCn mb += #fgC11 mb
scoreboard players operation #fgCn mb += #fgC12 mb
