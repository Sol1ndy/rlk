# #apR = 0..#apCn-1 -> the candidate whose weight range holds it.
scoreboard players set #apPick mb 0
execute if score #apPick mb matches 0 if score #apC1 mb matches 1.. if score #apR mb < #apC1 mb run scoreboard players set #apPick mb 1
scoreboard players operation #apR mb -= #apC1 mb
execute if score #apPick mb matches 0 if score #apC2 mb matches 1.. if score #apR mb < #apC2 mb run scoreboard players set #apPick mb 2
scoreboard players operation #apR mb -= #apC2 mb
execute if score #apPick mb matches 0 if score #apC3 mb matches 1.. if score #apR mb < #apC3 mb run scoreboard players set #apPick mb 3
scoreboard players operation #apR mb -= #apC3 mb
execute if score #apPick mb matches 0 if score #apC4 mb matches 1.. if score #apR mb < #apC4 mb run scoreboard players set #apPick mb 4
scoreboard players operation #apR mb -= #apC4 mb
execute if score #apPick mb matches 0 if score #apC5 mb matches 1.. if score #apR mb < #apC5 mb run scoreboard players set #apPick mb 5
scoreboard players operation #apR mb -= #apC5 mb
execute if score #apPick mb matches 0 if score #apC6 mb matches 1.. if score #apR mb < #apC6 mb run scoreboard players set #apPick mb 6
scoreboard players operation #apR mb -= #apC6 mb
execute if score #apPick mb matches 0 if score #apC31 mb matches 1.. if score #apR mb < #apC31 mb run scoreboard players set #apPick mb 31
scoreboard players operation #apR mb -= #apC31 mb
execute if score #apPick mb matches 0 if score #apC33 mb matches 1.. if score #apR mb < #apC33 mb run scoreboard players set #apPick mb 33
scoreboard players operation #apR mb -= #apC33 mb
execute if score #apPick mb matches 0 if score #apC34 mb matches 1.. if score #apR mb < #apC34 mb run scoreboard players set #apPick mb 34
scoreboard players operation #apR mb -= #apC34 mb
execute if score #apPick mb matches 0 if score #apC35 mb matches 1.. if score #apR mb < #apC35 mb run scoreboard players set #apPick mb 35
scoreboard players operation #apR mb -= #apC35 mb
