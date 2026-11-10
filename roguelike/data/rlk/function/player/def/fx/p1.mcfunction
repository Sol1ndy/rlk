# 1단계 패링 효과 (@s = 플레이어): 접점에 작은 금빛 불꽃만. 소리: 낮은 방패 막기
execute if entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.25 ~ facing entity @e[tag=rlk_hc_atk,limit=1] eyes positioned ^ ^ ^0.55 run function rlk:player/def/fx/p1_at
execute unless entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ~ ~1.25 ~ positioned ^ ^ ^0.55 run function rlk:player/def/fx/p1_at
