# A refilled bag never starts with the move just used.
scoreboard players set #rdSgB1_1 rd 1
scoreboard players set #rdSgB1_21 rd 1
scoreboard players set #rdSgB1_22 rd 1
scoreboard players set #rdSgB1_23 rd 1
scoreboard players set #rdSgB1_24 rd 1
scoreboard players set #rdSgB1_9 rd 1
scoreboard players set #rdSgB1_10 rd 1
execute if score @s rdPrev matches 1 run scoreboard players set #rdSgB1_1 rd 0
execute if score @s rdPrev matches 21 run scoreboard players set #rdSgB1_21 rd 0
execute if score @s rdPrev matches 22 run scoreboard players set #rdSgB1_22 rd 0
execute if score @s rdPrev matches 23 run scoreboard players set #rdSgB1_23 rd 0
execute if score @s rdPrev matches 24 run scoreboard players set #rdSgB1_24 rd 0
execute if score @s rdPrev matches 9 run scoreboard players set #rdSgB1_9 rd 0
execute if score @s rdPrev matches 10 run scoreboard players set #rdSgB1_10 rd 0
