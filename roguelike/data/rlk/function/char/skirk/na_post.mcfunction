# 일반 공격 한 번이 끝난 뒤 (@s = 플레이어, at 몸)
# 3타는 두 번 벤다: 3틱 뒤에 한 번 더
execute if score #skStep tmp matches 2 run scoreboard players set @s skQ 3
# 고갈: 적중했을 때만 횟수를 쓴다
execute if score #skDepUsed tmp matches 1 if score #hitLanded tmp matches 1 run function rlk:char/skirk/dep_use
# 일곱빛 섬광 중 마지막 타가 적중: 주변의 허계 균열 흡수
execute if score #skStep tmp matches 4.. if score @s skM matches 1.. if score #hitLanded tmp matches 1 run function rlk:char/skirk/absorb
