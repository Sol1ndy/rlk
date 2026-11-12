# 방전 한 대 (@s = 맞는 슬라임 두뇌): 작은 슬라임 = 최대 체력의 #c2ZapS %, 큰 슬라임 #c2ZapL %. 진짜 피해(원소 · 보정 없음, 면역 없음)
scoreboard players operation #c2zd tmp = @s mhpM
execute if entity @s[tag=rlk_cm_ss] run scoreboard players operation #c2zd tmp *= #c2ZapS tmp
execute unless entity @s[tag=rlk_cm_ss] run scoreboard players operation #c2zd tmp *= #c2ZapL tmp
scoreboard players operation #c2zd tmp /= #c2c100 tmp
execute if score #c2zd tmp matches ..0 run scoreboard players set #c2zd tmp 1
particle minecraft:electric_spark ~ ~0.6 ~ 0.2 0.3 0.2 0.2 8 normal
function rlk:cm/c2/true_hit
