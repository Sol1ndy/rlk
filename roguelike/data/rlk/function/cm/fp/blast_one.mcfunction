# 포자 폭발 한 대 (@s = 맞는 두뇌). 진짜 피해(보정 · 반응 없음, 면역 없음), 숫자는 풀 색
execute if entity @s[tag=rlk_c3pz] run return 0
tag @s add rlk_c3pz
scoreboard players operation #c2zd tmp = @s mhpM
execute if entity @s[tag=rlk_cm_fu] run function rlk:cm/fp/fu_mark
execute unless entity @s[tag=rlk_cm_fu] run function rlk:cm/fp/pct
particle minecraft:composter ~ ~0.8 ~ 0.25 0.3 0.25 0.1 8 normal
function rlk:cm/c3/true_hit
