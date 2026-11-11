# player/dodge/speed: 방향키를 누른 일반 닷지(내딛는 걸음), 남은 이동 틱 5 → 1
scoreboard players set #dgSp tmp 150
execute if score @s dashMoveT matches 5 run return run scoreboard players set #dgSp tmp 500
execute if score @s dashMoveT matches 4 run return run scoreboard players set #dgSp tmp 400
execute if score @s dashMoveT matches 3 run return run scoreboard players set #dgSp tmp 350
execute if score @s dashMoveT matches 2 run scoreboard players set #dgSp tmp 200
