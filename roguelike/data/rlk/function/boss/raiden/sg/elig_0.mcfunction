# Eligible = still in the bag; the guard (9) only after two other picks.
scoreboard players operation #rdSgE3 rd = #rdSgB0_3 rd
scoreboard players operation #rdSgE8 rd = #rdSgB0_8 rd
scoreboard players operation #rdSgE2 rd = #rdSgB0_2 rd
scoreboard players operation #rdSgE5 rd = #rdSgB0_5 rd
scoreboard players operation #rdSgE9 rd = #rdSgB0_9 rd
scoreboard players operation #rdSgE10 rd = #rdSgB0_10 rd
execute if score @s rdSgGd matches ..1 run scoreboard players set #rdSgE9 rd 0
scoreboard players set #rdSgCnt rd 0
execute if score #rdSgE3 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE8 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE2 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE5 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE9 rd matches 1 run scoreboard players add #rdSgCnt rd 1
execute if score #rdSgE10 rd matches 1 run scoreboard players add #rdSgCnt rd 1
