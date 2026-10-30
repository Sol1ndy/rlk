# 아랫줄 안내를 띄울 때 쓰는 빈 제목: F5 위쪽 시점이면 빈 제목 대신 조준점(받침에 탄 동안, 또는 선택 공간 안)
execute if score #on view matches 1 if score #vmode view matches 2 if entity @e[tag=rlk_vseat,limit=1] run return run title @s title [{"text":"","font":"rlk:hud","color":"white","shadow_color":0}]
execute if score #on view matches 1 if score #vmode view matches 2 if score @s pkMode matches 1.. unless score @s dead matches 1 unless score @s devMode matches 1 run return run title @s title [{"text":"","font":"rlk:hud","color":"white","shadow_color":0}]
title @s title {"text":""}
