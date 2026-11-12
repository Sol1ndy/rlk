# The hit count: #apArg (tests) or the 3 / 4 / 3 roll; the expected end on #apPLen.
scoreboard players operation #apq6 mb = #apArg mb
execute unless score #apq6 mb matches 2..4 store result score #apR mb run random value 0..9
execute unless score #apq6 mb matches 2..4 if score #apR mb matches 0..2 run scoreboard players set #apq6 mb 2
execute unless score #apq6 mb matches 2..4 if score #apR mb matches 3..6 run scoreboard players set #apq6 mb 3
execute unless score #apq6 mb matches 2..4 run scoreboard players set #apq6 mb 4
execute if score #apq6 mb matches 2 run scoreboard players set #apPLen mb 93
execute if score #apq6 mb matches 3 run scoreboard players set #apPLen mb 113
execute if score #apq6 mb matches 4 run scoreboard players set #apPLen mb 170
