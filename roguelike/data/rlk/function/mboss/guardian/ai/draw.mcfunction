# #gdR = 0..#gdCn-1 -> the #gdR-th candidate.
scoreboard players set #gdPick mb 0
execute if score #gdPick mb matches 0 if score #gdC1 mb matches 1 if score #gdR mb matches 0 run scoreboard players set #gdPick mb 1
execute if score #gdC1 mb matches 1 run scoreboard players remove #gdR mb 1
execute if score #gdPick mb matches 0 if score #gdC2 mb matches 1 if score #gdR mb matches 0 run scoreboard players set #gdPick mb 2
execute if score #gdC2 mb matches 1 run scoreboard players remove #gdR mb 1
execute if score #gdPick mb matches 0 if score #gdC3 mb matches 1 if score #gdR mb matches 0 run scoreboard players set #gdPick mb 3
execute if score #gdC3 mb matches 1 run scoreboard players remove #gdR mb 1
execute if score #gdPick mb matches 0 if score #gdC4 mb matches 1 if score #gdR mb matches 0 run scoreboard players set #gdPick mb 4
execute if score #gdC4 mb matches 1 run scoreboard players remove #gdR mb 1
execute if score #gdPick mb matches 0 if score #gdC5 mb matches 1 if score #gdR mb matches 0 run scoreboard players set #gdPick mb 5
execute if score #gdC5 mb matches 1 run scoreboard players remove #gdR mb 1
execute if score #gdPick mb matches 1 run scoreboard players set #gdBag1 mb 0
execute if score #gdPick mb matches 2 run scoreboard players set #gdBag2 mb 0
execute if score #gdPick mb matches 3 run scoreboard players set #gdBag3 mb 0
execute if score #gdPick mb matches 4 run scoreboard players set #gdBag4 mb 0
execute if score #gdPick mb matches 5 run scoreboard players set #gdBag5 mb 0
