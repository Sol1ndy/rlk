# 몸이 있던 쪽으로 도약(방향은 이 순간 고정)
scoreboard players set @s cmS 2
scoreboard players set @s cmT 9
scoreboard players set #c2Fw tmp 520
scoreboard players set #c2Up tmp 420
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/impulse
execute unless score #c2slleap snd matches 1 run function rlk:cm/c2/snd/slleap
