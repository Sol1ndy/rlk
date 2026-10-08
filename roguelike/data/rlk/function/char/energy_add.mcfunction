# 원소 에너지 획득 (@s = 플레이어, 입력: #enAdd tmp = 기본 획득량 × 100). 실제 = 기본 × 원소 충전 효율%
# 스커크: 원소 에너지 칸 = 뱀의 계략(스킬·허계 균열로만 얻음)
execute if score #charN tmp matches 3 run return 0
scoreboard players operation #enAdd tmp *= @s energyRecharge
scoreboard players operation #enAdd tmp /= #100 tmp
scoreboard players operation @s energy += #enAdd tmp
execute if score @s energy > #burstCost100 tmp run scoreboard players operation @s energy = #burstCost100 tmp
