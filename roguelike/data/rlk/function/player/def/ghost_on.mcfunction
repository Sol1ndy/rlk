# 퍼펙트 닷지 창 동안의 판정 자리 (rlk:tick 의 커스텀 몹 판정 · mboss/hz/hit_near · pj 와 나루카미의 근접 재판정): 몸 표시
# rlk_body 를 닷지를 시작한 자리의 표식(rlk_dgo)으로 옮긴다(진짜 몸은 rlk_body_real). 표식이 없으면 아무것도 안 함(#gh cb 0)
scoreboard players set #gh cb 0
execute unless entity @e[tag=rlk_dgo,limit=1] run return 0
scoreboard players set #gh cb 1
tag @e[tag=rlk_body] add rlk_body_real
tag @e[tag=rlk_body_real] remove rlk_body
tag @e[tag=rlk_dgo,limit=1] add rlk_body
