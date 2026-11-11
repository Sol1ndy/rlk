# player/dodge/speed: 더블 닷지의 두 번째 동작, 남은 이동 틱 6 → 1
scoreboard players set #dgSp tmp 150
execute if score @s dashMoveT matches 6 run return run scoreboard players set #dgSp tmp 250
execute if score @s dashMoveT matches 4..5 run return run scoreboard players set #dgSp tmp 400
execute if score @s dashMoveT matches 3 run return run scoreboard players set #dgSp tmp 350
execute if score @s dashMoveT matches 2 run scoreboard players set #dgSp tmp 250
