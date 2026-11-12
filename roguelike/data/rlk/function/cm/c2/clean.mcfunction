# 2챕터 무리 몹 모습 정리 (cm/clean 맨 앞): 두뇌가 사라진 리그 → 날아가며 터짐. 쓰러지는 리그는 ch1 정리에서 살려 둠
execute as @e[tag=rlk_c2root,tag=!rlk_cmsync,tag=!rlk_c2dying] at @s run function rlk:cm/c2/die
execute as @e[tag=rlk_c2root,tag=rlk_c2dying] at @s run function rlk:cm/c2/death_tick
execute if entity @e[tag=rlk_c2dying,limit=1] run tag @e[tag=rlk_c2dying] add rlk_cmsync
