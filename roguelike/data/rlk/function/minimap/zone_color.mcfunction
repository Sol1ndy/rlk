# As a zone marker: its colour code into #zc<zid>.
scoreboard players set #z mm 0
execute if score @s zst matches 1 run scoreboard players set #z mm 1
execute if score @s zst matches 2.. run scoreboard players set #z mm 2
execute if score @s zst matches 2.. if score @s zkind matches 2 run scoreboard players set #z mm 4
execute if score @s zst matches 2.. if score @s zkind matches 3 run scoreboard players set #z mm 5
execute if score @s zst matches 2.. if score @s zkind matches 4 run scoreboard players set #z mm 6
execute if score @s zst matches 2.. if score @s zkind matches 5 run scoreboard players set #z mm 7
execute if score @s zst matches 2.. if score @s zkind matches 6 run scoreboard players set #z mm 8
execute if score @s zst matches 2.. if score @s zkind matches 7 run scoreboard players set #z mm 9
execute if score @s zst matches 2.. if score @s zkind matches 8 run scoreboard players set #z mm 10
execute if score @s zst matches 2.. if score @s zkind matches 9 run scoreboard players set #z mm 11
execute if score @s zid = #pz mm run scoreboard players set #z mm 3
execute if score @s zid matches 1 run scoreboard players operation #zc1 mm = #z mm
execute if score @s zid matches 2 run scoreboard players operation #zc2 mm = #z mm
execute if score @s zid matches 3 run scoreboard players operation #zc3 mm = #z mm
execute if score @s zid matches 4 run scoreboard players operation #zc4 mm = #z mm
execute if score @s zid matches 5 run scoreboard players operation #zc5 mm = #z mm
execute if score @s zid matches 6 run scoreboard players operation #zc6 mm = #z mm
execute if score @s zid matches 7 run scoreboard players operation #zc7 mm = #z mm
execute if score @s zid matches 8 run scoreboard players operation #zc8 mm = #z mm
execute if score @s zid matches 9 run scoreboard players operation #zc9 mm = #z mm
execute if score @s zid matches 10 run scoreboard players operation #zc10 mm = #z mm
execute if score @s zid matches 11 run scoreboard players operation #zc11 mm = #z mm
execute if score @s zid matches 12 run scoreboard players operation #zc12 mm = #z mm
