# player/dodge/speed: 더블 닷지의 두 번째 동작(옆돌기), 남은 이동 틱 6 → 1
scoreboard players set #dgSp tmp 200
execute if score @s dashMoveT matches 6 run return run scoreboard players set #dgSp tmp 300
execute if score @s dashMoveT matches 3..5 run return run scoreboard players set #dgSp tmp 450
execute if score @s dashMoveT matches 2 run scoreboard players set #dgSp tmp 350
