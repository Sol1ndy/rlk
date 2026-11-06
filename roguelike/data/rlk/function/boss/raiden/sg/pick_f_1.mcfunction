execute store result score #rdSgR rd run random value 0..9999
scoreboard players operation #rdSgR rd %= #rdSgFc rd
scoreboard players add #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF1 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF1 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 1
execute if score @s rdPat matches 0 if score #rdSgF21 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF21 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 21
execute if score @s rdPat matches 0 if score #rdSgF22 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF22 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 22
execute if score @s rdPat matches 0 if score #rdSgF23 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF23 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 23
execute if score @s rdPat matches 0 if score #rdSgF24 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF24 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 24
execute if score @s rdPat matches 0 if score #rdSgF9 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF9 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 9
execute if score @s rdPat matches 0 if score #rdSgF10 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF10 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 10
