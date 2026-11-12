# @s = 퍼펙트 패링을 당한 공격자, at @s (2틱). 뒤로 젖혀진 반응: 그 보스의 모듈이 자기 자세를 가졌으면(레지스트리 "beat": mboss/d/beat_parried
# 가 1 을 돌려줌) 그것, 아니면 어느 리그에나 듣는 기본 반응 — 발밑 한 점에 모여 있는 리그 부품(레지스트리 보스의 rlk_mb_part ·
# 나루카미 rlk_raiden_part · 커스텀 몹의 rlk_cmlink)을 발을 축으로 16도 뒤로 기울이고 0.2칸 물린다(표시만: 판정 · 히트박스는 그대로).
# 레지스트리 보스는 사람 크기의 선 몸만(mboss/d/beat_rock: 파수꾼 · 아를레키노 · 타키 · 홍련 · 시험용): 길거나 누운 몸(야타용왕 · 아펩 · 나비 ·
# 장치)은 축에서 먼 끝이 크게 휘둘리므로 기울이지 않는다
scoreboard players set #btRk cb 1
scoreboard players set #t cb 0
execute if entity @s[tag=rlk_mb_body] store result score #t cb run function rlk:mboss/d/beat_parried
execute if score #t cb matches 1 run return 1
scoreboard players set #t cb 0
execute if entity @s[tag=rlk_mb_body] store result score #t cb run function rlk:mboss/d/beat_rock
execute if score #t cb matches 1 as @e[type=minecraft:item_display,tag=rlk_mb_part,distance=..6] at @s rotated ~ 0 run function rlk:player/def/beat/rock1
execute if entity @s[tag=rlk_raiden] as @e[type=minecraft:item_display,tag=rlk_raiden_part,distance=..6] at @s rotated ~ 0 run function rlk:player/def/beat/rock1
execute if entity @s[tag=rlk_cmb] run function rlk:player/def/beat/rock_cm
