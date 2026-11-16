execute store result score #rdSgR rd run random value 0..9999
scoreboard players operation #rdSgR rd %= #rdSgFc rd
scoreboard players add #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF3 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF3 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 3
execute if score @s rdPat matches 0 if score #rdSgF8 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF8 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 8
execute if score @s rdPat matches 0 if score #rdSgF2 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF2 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 2
execute if score @s rdPat matches 0 if score #rdSgF5 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF5 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 5
execute if score @s rdPat matches 0 if score #rdSgF9 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF9 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 9
execute if score @s rdPat matches 0 if score #rdSgF10 rd matches 1 run scoreboard players remove #rdSgR rd 1
execute if score @s rdPat matches 0 if score #rdSgF10 rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat 10
