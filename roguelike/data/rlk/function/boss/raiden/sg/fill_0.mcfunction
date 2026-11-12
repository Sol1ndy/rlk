# A refilled bag never starts with the move just used.
scoreboard players set #rdSgB0_3 rd 1
scoreboard players set #rdSgB0_8 rd 1
scoreboard players set #rdSgB0_2 rd 1
scoreboard players set #rdSgB0_5 rd 1
scoreboard players set #rdSgB0_9 rd 1
scoreboard players set #rdSgB0_10 rd 1
execute if score @s rdPrev matches 3 run scoreboard players set #rdSgB0_3 rd 0
execute if score @s rdPrev matches 8 run scoreboard players set #rdSgB0_8 rd 0
execute if score @s rdPrev matches 2 run scoreboard players set #rdSgB0_2 rd 0
execute if score @s rdPrev matches 5 run scoreboard players set #rdSgB0_5 rd 0
execute if score @s rdPrev matches 9 run scoreboard players set #rdSgB0_9 rd 0
execute if score @s rdPrev matches 10 run scoreboard players set #rdSgB0_10 rd 0
