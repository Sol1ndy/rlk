# 몸까지 돌진할 수 있는가 (@s, at @s): 6.5칸 안 · 1 / 2 / 3칸 앞 기둥이 지나갈 수 있음(벽 · 문 · 낭떠러지 아님)
execute unless entity @e[tag=rlk_body,distance=..6.5] run return 0
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1 unless function rlk:cm/c3/col_ok run return 0
execute if entity @e[tag=rlk_body,distance=2.2..] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^2 unless function rlk:cm/c3/col_ok run return 0
execute if entity @e[tag=rlk_body,distance=3.2..] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^3 unless function rlk:cm/c3/col_ok run return 0
return 1
