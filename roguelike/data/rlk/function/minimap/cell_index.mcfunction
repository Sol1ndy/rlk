# #cx/#cz block coordinates -> #idx = row * 6 + col (-1 outside the grid).
scoreboard players set #c20 mm 20
scoreboard players set #c6 mm 6
scoreboard players add #cx mm 60
scoreboard players add #cz mm 60
scoreboard players set #idx mm -1
execute unless score #cx mm matches 0..119 run return 0
execute unless score #cz mm matches 0..119 run return 0
scoreboard players operation #cx mm /= #c20 mm
scoreboard players operation #cz mm /= #c20 mm
scoreboard players operation #idx mm = #cz mm
scoreboard players operation #idx mm *= #c6 mm
scoreboard players operation #idx mm += #cx mm
