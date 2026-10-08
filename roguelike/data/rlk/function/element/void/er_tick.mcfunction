# 잠식 감소 (@s = 몹): 마지막으로 잠식을 받은 뒤 #rnErHold 틱이 지나면 1초에 1%씩
scoreboard players remove @s rnErT 1
execute if score @s rnErT matches 1.. run return 0
scoreboard players remove @s rnEr 1
scoreboard players set @s rnErT 20
