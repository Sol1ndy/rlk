# @s = 후보 몹. 공격 시작점에서 본 대상의 수평 방향을 비교한다.
# 월드 좌표를 점수로 변환하지 않아 멀리 떨어진 방에서도 좌표 오버플로가 없다.
scoreboard players set #meleeFront tmp 0
execute unless entity @e[tag=rlk_melee_origin,limit=1] run return 0
execute at @e[tag=rlk_melee_origin,limit=1] run tp @e[tag=rlk_melee_origin,limit=1] ~ ~ ~ facing entity @s feet
execute store result score #meleeDelta tmp run data get entity @e[tag=rlk_melee_origin,limit=1] Rotation[0] 100
scoreboard players operation #meleeDelta tmp -= #meleeYaw tmp
execute if score #meleeDelta tmp matches 18001.. run scoreboard players remove #meleeDelta tmp 36000
execute if score #meleeDelta tmp matches ..-18001 run scoreboard players add #meleeDelta tmp 36000
execute if score #meleeDelta tmp matches -9000..9000 run scoreboard players set #meleeFront tmp 1
