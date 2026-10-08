# 원소 반응이 일어남 (@s = 맞은 몹, at @s, #rx = 반응 번호). 빙결(6)·초전도(4)·얼음 확산(8)·얼음 결정(9)이면 몸 주변에 허계 균열 (간격 #skRiftCdT, 최대 3개)
execute unless entity @s[tag=rlk_mob] run return 0
scoreboard players set #ok tmp 0
execute if score #rx tmp matches 6 run scoreboard players set #ok tmp 1
execute if score #rx tmp matches 4 run scoreboard players set #ok tmp 1
execute if score #rx tmp matches 8..9 if score @s rxEl matches 4 run scoreboard players set #ok tmp 1
execute if score #ok tmp matches 0 run return 0
execute if score #skRiftCd tmp matches 1.. run return 0
execute store result score #t1 tmp if entity @e[tag=rlk_rift]
execute if score #t1 tmp matches 3.. run return 0
scoreboard players operation #skRiftCd tmp = #skRiftCdT tmp
# 몸 주변의 무작위 방향·거리(2~4칸)에 생성
execute store result storage rlk:tmp rift.yaw int 1 run random value 0..359
execute store result storage rlk:tmp rift.d int 1 run random value 2..4
execute at @e[tag=rlk_body,limit=1] run function rlk:char/skirk/rift_at with storage rlk:tmp rift
