# 북 가속 중 (@s = 두뇌): 10틱마다 3틱은 한 틱 더(#c2X 1) = 타이머 x1.3. 무리 몹은 이동 +30%(rlk:cm_haste)와 쿨타임 한 틱 더
scoreboard players add @s c2H 1
execute if score @s c2H matches 10.. run scoreboard players set @s c2H 0
execute if score @s c2H matches 2 run scoreboard players set #c2X tmp 1
execute if score @s c2H matches 5 run scoreboard players set #c2X tmp 1
execute if score @s c2H matches 8 run scoreboard players set #c2X tmp 1
execute if entity @s[tag=rlk_c2a,tag=!rlk_c2hm] run function rlk:cm/c2/haste_add
execute if score #c2X tmp matches 1 if entity @s[tag=rlk_c2a] if score @s cmCd matches 1.. run scoreboard players remove @s cmCd 1
