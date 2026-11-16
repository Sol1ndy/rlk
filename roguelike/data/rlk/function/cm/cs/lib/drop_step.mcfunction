execute at @s unless block ~ ~-0.25 ~ #rlk:cm_pass run return 0
execute at @s run tp @s ~ ~-0.25 ~
scoreboard players remove #wD tmp 1
execute if score #wD tmp matches 1.. run function rlk:cm/cs/lib/drop_step
