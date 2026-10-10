# 포탄 폭발: 몸이 2.2칸 안이면 폭발 피해. 부술 수 있는 장애물(바닥·벽 제외)을 3×3×3 부숨
particle minecraft:explosion ~ ~0.3 ~ 0.4 0.2 0.4 0 3
particle minecraft:large_smoke ~ ~0.5 ~ 0.7 0.3 0.7 0.03 14
execute unless score #k87 snd matches 1 run function rlk:snd/f94
execute positioned ~ ~0.2 ~ if entity @e[tag=rlk_body,distance=..2.2] run function rlk:cm/hit_pj
function rlk:cm/brk_here {r:1,yl:-1,yh:1}
function rlk:cm/wd_kill
kill @s
