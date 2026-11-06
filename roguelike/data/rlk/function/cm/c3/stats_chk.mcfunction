# 3챕터 몹 1레벨 체력 · 처치 경험치 (@s = 새 두뇌, room/mob_init 에서). 정예 id 도 여기서 rlk_c3 를 받음
execute if entity @s[tag=rlk_cm_cs] run tag @s add rlk_c3
execute if entity @s[tag=rlk_cm_rv] run tag @s add rlk_c3
execute if entity @s[tag=rlk_cm_pc] run tag @s add rlk_c3
execute if entity @s[tag=rlk_c3] run function rlk:cm/c3/stats
