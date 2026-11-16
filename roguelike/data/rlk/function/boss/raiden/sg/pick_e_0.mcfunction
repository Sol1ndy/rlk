execute store result score #rdSgR rd run random value 0..9999
scoreboard players operation #rdSgR rd %= #rdSgCnt rd
scoreboard players add #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE3 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE3 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 3
execute if score @s rdPat matches 0 if score #rdSgE8 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE8 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 8
execute if score @s rdPat matches 0 if score #rdSgE2 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE2 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 2
execute if score @s rdPat matches 0 if score #rdSgE5 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE5 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 5
execute if score @s rdPat matches 0 if score #rdSgE9 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE9 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 9
execute if score @s rdPat matches 0 if score #rdSgE10 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE10 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 10
