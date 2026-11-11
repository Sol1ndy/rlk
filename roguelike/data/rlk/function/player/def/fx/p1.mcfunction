# 1단계 패링 효과 (@s = 플레이어): 원작의 일반 가드처럼 — 접점에 아주 작은 노란 불꽃(g/spark, 3틱)과 가늘고 짧은 "틱" 소리뿐.
# 멈춤 · 가로 줄 · 화면 빛 · 큰 별빛은 퍼펙트 패링(fx/p3)에만 있다: 한눈에 "막았지만 퍼펙트는 아니다"
execute if entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.25 ~ facing entity @e[tag=rlk_hc_atk,limit=1] eyes positioned ^ ^ ^0.55 run function rlk:player/def/fx/p1_at
execute unless entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ~ ~1.25 ~ positioned ^ ^ ^0.55 run function rlk:player/def/fx/p1_at
