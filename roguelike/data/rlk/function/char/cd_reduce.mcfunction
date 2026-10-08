# 스킬 재사용 대기 감소 효과(모래시계 조각 · 각인 순환) — 캐릭터가 skillCd 를 직접 넣은 뒤에 부른다 (@s = 플레이어)
execute if score @s it_hourglass_shard matches 1.. run function rlk:items/proc/hourglass
execute if score cycle engN matches 2.. run function rlk:engravings/cycle/cd
