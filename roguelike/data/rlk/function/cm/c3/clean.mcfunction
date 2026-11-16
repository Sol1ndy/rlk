# 3챕터 무리 몹 모습 정리 (cm/clean 맨 앞): 두뇌가 사라진 리그 → 날아가며 터짐. 쓰러지는 리그는 ch1 정리에서 살려 둠
# 포자 주머니(fp)는 두뇌가 아니라서 여기서 한 틱씩 돈다(마지막 몹이 죽은 뒤에도 사라질 때까지)
execute as @e[tag=rlk_c3pod] at @s run function rlk:cm/fp/tick
execute as @e[tag=rlk_c3root,tag=!rlk_cmsync,tag=!rlk_c3dying] at @s run function rlk:cm/c3/die
execute as @e[tag=rlk_c3root,tag=rlk_c3dying] at @s run function rlk:cm/c3/death_tick
execute if entity @e[tag=rlk_c3dying,limit=1] run tag @e[tag=rlk_c3dying] add rlk_cmsync
