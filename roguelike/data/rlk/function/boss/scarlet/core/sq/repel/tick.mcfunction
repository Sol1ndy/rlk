# Stand-in repel tick (#sq hr 1..104).
execute if score #sq hr matches 24 run scoreboard players set #sq_sig hr 1
execute if score #sq hr matches 75 run scoreboard players set #sq_sig hr 2
execute if score #sq hr matches 102 run scoreboard players set #sq_sig hr 3
execute if score #sq hr matches 104.. run scoreboard players set #sqdone hr 1
