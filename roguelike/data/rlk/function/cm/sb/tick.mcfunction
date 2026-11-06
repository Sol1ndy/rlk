# 모래 전갈 새끼 (@s, at @s). 순환: 땅속(#c3Dn_sb) → 몸 둘레 고리 자리에 모래 둔덕(예고 0.8초) → 솟구쳐 물기(8) → 땅 위 2초(반격 시간) → 다시 파고듦.
# 걷지 않음(자리 이동은 솟을 때 한 번). 빙결 중에는 순환이 멈춤(땅 위에서만 얼 수 있음)
scoreboard players set #hold tmp 1
execute if score @s frzT matches 1.. run return 0
scoreboard players remove @s c2T 1
execute if score @s c3B matches 0 run return run function rlk:cm/sb/under
execute if score @s c3B matches 1 run return run function rlk:cm/sb/mound
execute if score @s c3B matches 2 run return run function rlk:cm/sb/up
execute if score @s c3B matches 3 run return run function rlk:cm/sb/sink
