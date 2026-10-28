# 2챕터 몹 1레벨 체력 · 처치 경험치 (@s = 새 두뇌, room/mob_init 에서). 정예 id 도 여기서 rlk_c2 를 받음
execute if entity @s[tag=rlk_cm_kr] run tag @s add rlk_c2
execute if entity @s[tag=rlk_cm_nj] run tag @s add rlk_c2
execute if entity @s[tag=rlk_cm_cc] run tag @s add rlk_c2
execute if entity @s[tag=rlk_cm_ci] run tag @s add rlk_c2
execute if entity @s[tag=rlk_c2] run function rlk:cm/c2/stats
