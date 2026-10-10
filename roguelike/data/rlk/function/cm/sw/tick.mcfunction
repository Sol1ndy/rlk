# 검사: 붙으면 짧은 선딜 후 베기(1.5초마다). 선딜 중 경직되면 취소
execute if score @s cmS matches 1 run return run function rlk:cm/sw/wind
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..2.6] run function rlk:cm/sw/start
