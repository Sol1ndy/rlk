# 2단계 패링 효과 (@s = 플레이어): 원작의 일반 가드 — 접점에 작은 노란 불꽃(g/spark, 3틱; 1단계보다 조금 큼)과 떨어지는 불티 몇 개, 가늘고
# 짧은 "틱" 소리. 화면 덮개 · 섬광 · 별빛 없음(11-11b 판은 퍼펙트와 같은 별빛 · 화면 번쩍임 · 줄이라 구분되지 않았다)
execute if entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.25 ~ facing entity @e[tag=rlk_hc_atk,limit=1] eyes positioned ^-0.45 ^0.5 ^0.6 run function rlk:player/def/fx/p2_at
execute unless entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ~ ~1.25 ~ positioned ^-0.45 ^0.5 ^0.6 run function rlk:player/def/fx/p2_at
