# Into the pattern slot: p/run starts it this tick (pattern clock 0 = clip tick 0).
scoreboard players set #fgSt mb 1
scoreboard players operation #fgPat mb = #fgPick mb
scoreboard players set #fgPNew mb 1
execute unless score #fgMv mb matches 0 run scoreboard players set #fgMv mb 0
execute if score #fgPick mb matches 1 run scoreboard players add #fgCruN mb 1
execute if score #fgPick mb matches 2 run scoreboard players add #fgCruN mb 1
execute if score #fgPick mb matches 3 run scoreboard players add #fgCruN mb 1
execute if score #fgPick mb matches 4 run scoreboard players add #fgCruN mb 1
execute if score #fgPick mb matches 5 run scoreboard players add #fgCruN mb 1
execute if score #fgPick mb matches 6 run scoreboard players add #fgCruN mb 1
