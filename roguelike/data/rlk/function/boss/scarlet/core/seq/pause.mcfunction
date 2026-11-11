# A sequence was running when the fight froze (@s = body): what resume does (#grs). CS0 (also its replay) -> 9;
# CS1 -> 6; the repel -> 7; a lead-in -> 8.
execute if score #sqn hr matches 1 run return run scoreboard players set #grs hr 9
execute if score #sqn hr matches 2 run return run scoreboard players set #grs hr 6
execute if score #sqn hr matches 4 run return run scoreboard players set #grs hr 7
execute if score #sqn hr matches 3 run return run scoreboard players set #grs hr 8
execute if score #sqn hr matches 5 run return run scoreboard players set #grs hr 8
execute if score #sqn hr matches 6 run return run scoreboard players set #grs hr 8
