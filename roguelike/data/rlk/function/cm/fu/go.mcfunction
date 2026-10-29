# 몸이 있던 쪽으로 툭 박치기(4틱, 방향은 이 순간 고정)
scoreboard players set @s cmS 2
scoreboard players set @s cmT 4
scoreboard players set @s c2T2 0
scoreboard players set #c2Fw tmp 420
scoreboard players set #c2Up tmp 120
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/impulse
execute unless score #c3fubump snd matches 1 run function rlk:cm/c3/snd/fubump
