# #fgR = 0..#fgCn-1 (sum of the weights) -> the candidate whose weight range holds it.
scoreboard players set #fgPick mb 0
execute if score #fgPick mb matches 0 if score #fgC11 mb matches 1.. if score #fgR mb < #fgC11 mb run scoreboard players set #fgPick mb 11
scoreboard players operation #fgR mb -= #fgC11 mb
execute if score #fgPick mb matches 0 if score #fgC12 mb matches 1.. if score #fgR mb < #fgC12 mb run scoreboard players set #fgPick mb 12
scoreboard players operation #fgR mb -= #fgC12 mb
execute if score #fgPick mb matches 11 run scoreboard players set #fgBag11 mb 0
execute if score #fgPick mb matches 12 run scoreboard players set #fgBag12 mb 0
