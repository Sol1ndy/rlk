execute store result score #rdSgR rd run random value 0..9999
scoreboard players operation #rdSgR rd %= #rdSgCnt rd
scoreboard players add #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE1 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE1 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 1
execute if score @s rdPat matches 0 if score #rdSgE21 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE21 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 21
execute if score @s rdPat matches 0 if score #rdSgE22 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE22 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 22
execute if score @s rdPat matches 0 if score #rdSgE23 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE23 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 23
execute if score @s rdPat matches 0 if score #rdSgE24 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE24 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 24
execute if score @s rdPat matches 0 if score #rdSgE9 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE9 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 9
execute if score @s rdPat matches 0 if score #rdSgE10 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgE10 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 10
