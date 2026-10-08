# 풀 이슬 (@s = 플레이어, 창이 열려 있는 동안): 매 틱 100(+모래의 딸 보너스)씩 쌓여 #nfDewGap 마다 1개(최대 3)
scoreboard players remove @s nfDewW 1
scoreboard players set #t1 tmp 100
# 모래의 딸: 그림자 춤 중 원소 마스터리 300 초과분 100당 +10 (최대 +50)
execute if score @s nfSD matches 1.. run function rlk:char/nefer/sand_bonus
scoreboard players operation @s nfDewT += #t1 tmp
execute if score @s nfDewT >= #nfDewGap tmp run function rlk:char/nefer/dew_gain
execute if score @s nfDewW matches ..0 run scoreboard players set @s nfDewT 0
