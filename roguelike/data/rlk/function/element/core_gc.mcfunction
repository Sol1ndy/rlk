# 본체(풀 원핵 · 기만의 핵)가 없어진 모델 조각을 치운다
tag @e[tag=rlk_coreP] add rlk_orph
execute as @e[tag=rlk_core] on passengers run tag @s remove rlk_orph
execute as @e[tag=rlk_dcore] on passengers run tag @s remove rlk_orph
kill @e[tag=rlk_orph]
