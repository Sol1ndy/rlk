# cmYaw 를 몸 쪽으로 최대 #cmTurn(0.01°)만큼 돌림
execute facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score #yd tmp run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
scoreboard players operation #yd tmp -= @s cmYaw
execute if score #yd tmp matches 18001.. run scoreboard players remove #yd tmp 36000
execute if score #yd tmp matches ..-18001 run scoreboard players add #yd tmp 36000
scoreboard players operation #yd tmp < #cmTurn tmp
scoreboard players operation #yd tmp > #cmTurnN tmp
scoreboard players operation @s cmYaw += #yd tmp
execute if score @s cmYaw matches 18001.. run scoreboard players remove @s cmYaw 36000
execute if score @s cmYaw matches ..-18001 run scoreboard players add @s cmYaw 36000
