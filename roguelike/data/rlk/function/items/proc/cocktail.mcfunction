scoreboard players set #t1 itv 0
execute if score @s shieldHP matches 1.. run scoreboard players set #t1 itv 1
execute if score @s gShield matches 1.. run scoreboard players set #t1 itv 1
execute if score #t1 itv matches 1 run scoreboard players operation @s moveSpeed += #cocktailSpd tmp
execute if score #t1 itv matches 1 run scoreboard players operation @s atkSpeed += #cocktailSpd tmp
