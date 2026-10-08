# 일반 공격 한 번이 끝난 뒤 (@s = 플레이어, at 몸): 여러 번 치는 타면 3틱마다 한 번 더(#naX2 번)
execute if score #naX2 tmp matches 1.. run scoreboard players set @s naQ 3
execute if score #naX2 tmp matches 1.. run scoreboard players operation @s naQc = #coef tmp
execute if score #naX2 tmp matches 1.. run scoreboard players operation @s naQn = #naX2 tmp
execute if score #charN tmp matches 5 run function rlk:char/arlecchino/na_post
