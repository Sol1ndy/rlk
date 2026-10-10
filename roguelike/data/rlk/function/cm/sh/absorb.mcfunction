# 방패 (@s = 방패병 두뇌, combat/apply 에서): 몸이 방패 방향(cmYaw) ±60° 안에 있으면 내구도가 피해를 먼저 받음
execute facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score #yd tmp run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
scoreboard players operation #yd tmp -= @s cmYaw
execute if score #yd tmp matches 18001.. run scoreboard players remove #yd tmp 36000
execute if score #yd tmp matches ..-18001 run scoreboard players add #yd tmp 36000
execute if score #yd tmp matches ..-1 run scoreboard players operation #yd tmp *= #m1 tmp
execute if score #yd tmp matches 6001.. run return 0
scoreboard players set #cmBlk tmp 1
scoreboard players operation #t1 tmp = #dmg tmp
scoreboard players operation #t1 tmp < @s cmSh
scoreboard players operation @s cmSh -= #t1 tmp
scoreboard players operation #dmg tmp -= #t1 tmp
execute if score #dmg tmp matches ..0 run data modify storage rlk:combat col set value "#9FD8FF"
particle minecraft:electric_spark ~ ~1.3 ~ 0.3 0.4 0.3 0.1 6
execute unless score #k97 snd matches 1 run function rlk:snd/f104
execute if score @s cmSh matches ..0 run function rlk:cm/sh/break
