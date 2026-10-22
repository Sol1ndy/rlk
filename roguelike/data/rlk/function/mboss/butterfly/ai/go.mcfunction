# Into the pattern slot: p/run starts it this tick (pattern clock 0 = clip tick 0).
scoreboard players set #bfSt mb 1
scoreboard players operation #bfPat mb = #bfPick mb
scoreboard players set #bfPNew mb 1
execute if score #bfPick mb matches 1 run scoreboard players add #bfHumN mb 1
execute if score #bfPick mb matches 2 run scoreboard players add #bfHumN mb 1
execute if score #bfPick mb matches 3 run scoreboard players add #bfHumN mb 1
execute if score #bfPick mb matches 4 run scoreboard players add #bfHumN mb 1
execute if score #bfPick mb matches 11 run scoreboard players add #bfBfN mb 1
execute if score #bfPick mb matches 12 run scoreboard players add #bfBfN mb 1
execute if score #bfPick mb matches 13 run scoreboard players add #bfBfN mb 1
execute if score #bfPick mb matches 14 run scoreboard players add #bfBfN mb 1
