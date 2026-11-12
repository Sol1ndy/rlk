# #bfR = 0..#bfCn-1 (sum of the weights) -> the candidate whose weight range holds it.
scoreboard players set #bfPick mb 0
execute if score #bfPick mb matches 0 if score #bfC11 mb matches 1.. if score #bfR mb < #bfC11 mb run scoreboard players set #bfPick mb 11
scoreboard players operation #bfR mb -= #bfC11 mb
execute if score #bfPick mb matches 0 if score #bfC12 mb matches 1.. if score #bfR mb < #bfC12 mb run scoreboard players set #bfPick mb 12
scoreboard players operation #bfR mb -= #bfC12 mb
execute if score #bfPick mb matches 0 if score #bfC13 mb matches 1.. if score #bfR mb < #bfC13 mb run scoreboard players set #bfPick mb 13
scoreboard players operation #bfR mb -= #bfC13 mb
execute if score #bfPick mb matches 0 if score #bfC14 mb matches 1.. if score #bfR mb < #bfC14 mb run scoreboard players set #bfPick mb 14
scoreboard players operation #bfR mb -= #bfC14 mb
execute if score #bfPick mb matches 11 run scoreboard players set #bfBag11 mb 0
execute if score #bfPick mb matches 12 run scoreboard players set #bfBag12 mb 0
execute if score #bfPick mb matches 13 run scoreboard players set #bfBag13 mb 0
execute if score #bfPick mb matches 14 run scoreboard players set #bfBag14 mb 0
