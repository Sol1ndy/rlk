# The HP floors (absolute) from her max HP (@s = body): #fl60 = 600 per mille, #fl5 = 50.
scoreboard players operation #fl60 hr = @s mhpM
scoreboard players set #t5 hr 600
scoreboard players set #t4 hr 0
execute if score #fl60 hr matches ..2000000 run scoreboard players set #t4 hr 1
execute if score #t4 hr matches 1 run scoreboard players operation #fl60 hr *= #t5 hr
scoreboard players operation #fl60 hr /= #c1000 hr
execute if score #t4 hr matches 0 run scoreboard players operation #fl60 hr *= #t5 hr
execute if score #fl60 hr matches ..0 run scoreboard players set #fl60 hr 1
scoreboard players operation #fl5 hr = @s mhpM
scoreboard players set #t5 hr 50
scoreboard players set #t4 hr 0
execute if score #fl5 hr matches ..2000000 run scoreboard players set #t4 hr 1
execute if score #t4 hr matches 1 run scoreboard players operation #fl5 hr *= #t5 hr
scoreboard players operation #fl5 hr /= #c1000 hr
execute if score #t4 hr matches 0 run scoreboard players operation #fl5 hr *= #t5 hr
execute if score #fl5 hr matches ..0 run scoreboard players set #fl5 hr 1
