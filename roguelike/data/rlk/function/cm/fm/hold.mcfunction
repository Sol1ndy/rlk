# 들고 있는 화염구를 머리 위 세 자리에
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_cmfbh,distance=..6] if score @s cmId = #cid tmp run function rlk:cm/fm/slot
