# 마지막 구역 (@s = 구역 표식, at @s): 다음 맵 선택 오브젝트. 4번째 맵까지는 무작위 3개(이번 챕터에 이미 들어간 종류 제외, 재련 예외), 그 다음은 보스전
execute if score #mapIdx room matches 4.. run return run function rlk:room/end_boss
# ----- 재련(6) 맵 규칙 -----
# #rfCount = 이번 런에서 재련 맵을 '고른' 횟수(최대 #rfMax). 안 고르면 횟수는 그대로라 다음 선택지에 또 나올 수 있다
# 2챕터의 마지막 선택(보스전 직전 선택, #mapIdx 3)에는 아직 횟수가 남아 있으면 반드시 나오고, 3챕터부터는 나오지 않는다
execute unless score #rfCount room matches 0.. run scoreboard players set #rfCount room 0
scoreboard players set #rfForce tmp 0
execute if score #chapter room matches 2 if score #mapIdx room matches 3 if score #rfCount room < #rfMax tmp run scoreboard players set #rfForce tmp 1
# 무작위 후보에서 빼는 경우: 이미 다 골랐음 / 3챕터 이후 / 이번에 강제로 넣음 (pool[5] = 재련)
scoreboard players set #rfOut tmp 0
execute if score #rfCount room >= #rfMax tmp run scoreboard players set #rfOut tmp 1
execute if score #chapter room matches 3.. run scoreboard players set #rfOut tmp 1
execute if score #rfForce tmp matches 1 run scoreboard players set #rfOut tmp 1
# 후보 목록: 이번 챕터에 이미 들어간 종류는 뺀다(재련 6 은 위의 재련 규칙으로만)
data modify storage rlk:room pool set value []
execute unless score #seen1 room matches 1 run data modify storage rlk:room pool append value 1
execute unless score #seen2 room matches 1 run data modify storage rlk:room pool append value 2
execute unless score #seen3 room matches 1 run data modify storage rlk:room pool append value 3
execute unless score #seen4 room matches 1 run data modify storage rlk:room pool append value 4
execute unless score #seen5 room matches 1 run data modify storage rlk:room pool append value 5
execute unless score #rfOut tmp matches 1 run data modify storage rlk:room pool append value 6
execute unless score #seen7 room matches 1 run data modify storage rlk:room pool append value 7
# 혹시 후보가 3개보다 적으면(정상 진행에선 없음) 들어갔던 종류도 다시 넣는다
execute store result score #n tmp run data get storage rlk:room pool
execute if score #n tmp matches ..2 run data modify storage rlk:room pool set value [1,2,3,4,5,7]
# 강제로 넣을 때는 세 자리 중 무작위 한 자리
scoreboard players set #rfSlot tmp -1
execute if score #rfForce tmp matches 1 store result score #rfSlot tmp run random value 0..2
execute positioned ~-5 ~ ~ unless score #rfSlot tmp matches 0 run function rlk:room/choice
execute positioned ~-5 ~ ~ if score #rfSlot tmp matches 0 run function rlk:room/choice_reforge
execute positioned ~ ~ ~ unless score #rfSlot tmp matches 1 run function rlk:room/choice
execute positioned ~ ~ ~ if score #rfSlot tmp matches 1 run function rlk:room/choice_reforge
execute positioned ~5 ~ ~ unless score #rfSlot tmp matches 2 run function rlk:room/choice
execute positioned ~5 ~ ~ if score #rfSlot tmp matches 2 run function rlk:room/choice_reforge
