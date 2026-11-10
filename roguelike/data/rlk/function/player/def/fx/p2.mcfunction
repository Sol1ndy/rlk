# 2단계 패링 효과 (@s = 플레이어): 접점에 작은 금빛 번쩍임(작은 별빛) · 불꽃, 화면 가운데 짧은 줄(g/title streak_s, 4틱). 소리: 방패 막기 · 치명타
execute if entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.25 ~ facing entity @e[tag=rlk_hc_atk,limit=1] eyes positioned ^ ^ ^0.55 run function rlk:player/def/fx/p2_at
execute unless entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ~ ~1.25 ~ positioned ^ ^ ^0.55 run function rlk:player/def/fx/p2_at
function rlk:player/def/fx/ovl {g:"streak_s",in:0,hold:2,out:2,t:4}
