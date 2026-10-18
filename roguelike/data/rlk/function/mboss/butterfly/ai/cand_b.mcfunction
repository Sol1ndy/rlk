# Candidates (b): in the bag, allowed in the current range band, not the last one.
# #bfC<id> = its draw weight in this band (0 = no candidate).
scoreboard players set #bfC11 mb 0
execute if score #bfBag11 mb matches 1 if score #bfBand mb matches 1 unless score #bfLast mb matches 11 run scoreboard players set #bfC11 mb 2
execute if score #bfBag11 mb matches 1 if score #bfBand mb matches 2 unless score #bfLast mb matches 11 run scoreboard players set #bfC11 mb 1
scoreboard players set #bfC12 mb 0
execute if score #bfBag12 mb matches 1 if score #bfBand mb matches 2 unless score #bfLast mb matches 12 run scoreboard players set #bfC12 mb 1
execute if score #bfBag12 mb matches 1 if score #bfBand mb matches 3 unless score #bfLast mb matches 12 run scoreboard players set #bfC12 mb 2
scoreboard players set #bfC13 mb 0
execute if score #bfBag13 mb matches 1 if score #bfBand mb matches 1 unless score #bfLast mb matches 13 run scoreboard players set #bfC13 mb 1
execute if score #bfBag13 mb matches 1 if score #bfBand mb matches 2 unless score #bfLast mb matches 13 run scoreboard players set #bfC13 mb 2
scoreboard players set #bfC14 mb 0
execute if score #bfBag14 mb matches 1 if score #bfBand mb matches 2 unless score #bfLast mb matches 14 run scoreboard players set #bfC14 mb 1
execute if score #bfBag14 mb matches 1 if score #bfBand mb matches 3 unless score #bfLast mb matches 14 run scoreboard players set #bfC14 mb 1
scoreboard players set #bfCn mb 0
scoreboard players operation #bfCn mb += #bfC11 mb
scoreboard players operation #bfCn mb += #bfC12 mb
scoreboard players operation #bfCn mb += #bfC13 mb
scoreboard players operation #bfCn mb += #bfC14 mb
