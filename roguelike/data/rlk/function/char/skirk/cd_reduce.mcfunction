# 스킬 재사용 대기 감소 효과(모래시계 조각 · 각인 순환) — char/cast_skill 과 같은 처리
execute if score @s it_hourglass_shard matches 1.. run function rlk:items/proc/hourglass
execute if score cycle engN matches 2.. run function rlk:engravings/cycle/cd
