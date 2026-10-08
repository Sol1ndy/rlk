# 일곱빛 섬광 중의 일반 공격 (@s = 플레이어, 피해 계산 직후): 다른 원소 부여로 바뀌지 않는 얼음 원소 + 고갈(진)의 피해 증가
scoreboard players set #elem tmp 4
execute if score @s skDep matches 1.. unless score @s skDepCd matches 1.. run function rlk:char/skirk/dep_amp
