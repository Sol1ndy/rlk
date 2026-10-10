# 아랫줄 안내를 띄울 때 쓰는 빈 제목: F5 위쪽 시점이면 빈 제목 대신 조준점
execute if score #on view matches 1 if score #vmode view matches 2 if entity @e[tag=rlk_vseat,limit=1] run return run title @s title [{"text":"\ue100\ue101","font":"rlk:hud","color":"white","shadow_color":0}]
title @s title {"text":""}
