# player/dodge/speed: 공격을 피한 닷지의 백스텝, 남은 이동 틱 4 → 1
scoreboard players set #dgSp tmp 400
execute if score @s dashMoveT matches 4 run return run scoreboard players set #dgSp tmp 900
execute if score @s dashMoveT matches 3 run return run scoreboard players set #dgSp tmp 800
execute if score @s dashMoveT matches 2 run scoreboard players set #dgSp tmp 600
