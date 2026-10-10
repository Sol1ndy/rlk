# 체험 방 (@s = 플레이어)
# 쿨타임 · 에너지 무한
execute if score #lobInf lob matches 1 run scoreboard players set @s skillCd 0
execute if score #lobInf lob matches 1 run scoreboard players set @s burstCd 0
execute if score #lobInf lob matches 1 run scoreboard players operation @s energy = #burstCost100 tmp
# 더미 원소(2초마다)
execute store result score #t lob run time query gametime
scoreboard players operation #t lob %= #c40 lob
execute if score #t lob matches 0 if score #lobAura lob matches 1.. run function rlk:lobby/try/aura_put
# DPS: 피해가 들어오면 기록. 3초 동안 피해가 없으면 시간을 멈추고, 그 뒤 다시 때리면 새로 잰다
execute if score #dd lob matches 1.. run function rlk:lobby/try/hit
execute if score #dpsOn lob matches 1 run scoreboard players add #dpsIdle lob 1
execute if score #dpsOn lob matches 1 if score #dpsIdle lob matches ..60 run scoreboard players add #dpsT lob 1
# 멈출 때: 마지막 타격 뒤 기다린 3초는 시간에서 뺌
execute if score #dpsOn lob matches 1 if score #dpsIdle lob matches 61 run scoreboard players remove #dpsT lob 60
execute if score #dpsOn lob matches 1 if score #dpsIdle lob matches 61 if score #dpsT lob matches ..0 run scoreboard players set #dpsT lob 1
execute if score #dpsOn lob matches 1 if score #dpsIdle lob matches 61 run function rlk:lobby/try/board
scoreboard players add #dpsR lob 1
execute if score #dpsR lob matches 5.. run function rlk:lobby/try/board
