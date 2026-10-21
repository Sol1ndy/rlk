# Eligible = still in the bag; the guard (9) only after two other picks.
scoreboard players operation #rdSgE1 rd = #rdSgB1_1 rd
scoreboard players operation #rdSgE21 rd = #rdSgB1_21 rd
scoreboard players operation #rdSgE22 rd = #rdSgB1_22 rd
scoreboard players operation #rdSgE23 rd = #rdSgB1_23 rd
scoreboard players operation #rdSgE24 rd = #rdSgB1_24 rd
scoreboard players operation #rdSgE9 rd = #rdSgB1_9 rd
scoreboard players operation #rdSgE10 rd = #rdSgB1_10 rd
execute if score @s rdSgGd matches ..1 run scoreboard players set #rdSgE9 rd 0
scoreboard players set #rdSgCnt rd 0
execute if score #rdSgE1 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE21 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE22 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE23 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE24 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE9 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE10 rd matches 1 run scoreboard players add #rdSgCnt rd 1
