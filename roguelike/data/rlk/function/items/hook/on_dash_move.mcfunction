# 대쉬 이동 중 매 틱 (@s = 플레이어, at @s)
# 마검 키리온: 대쉬 경로에 2틱 간격으로 참격 마커 → 지나온 자리에서 순차 발동
scoreboard players operation #kmod tmp = @s dashMoveT
scoreboard players operation #kmod tmp %= #st2 tmp
execute if score @s it_sword_kirion matches 1.. if score #kmod tmp matches 0 at @e[tag=rlk_body,limit=1] run function rlk:items/proc/kirion_dash_mark
# 각인 질주 4개: 지나친 적에게 바람 원소 피해
execute if score dash engN matches 4.. at @e[tag=rlk_body,limit=1] if entity @e[tag=rlk_mob,tag=!rlk_dhit,distance=..2.2,limit=1] run function rlk:engravings/dash/hit
# 생명줄: 지나친 적에게 실
execute if score @s it_lifeline matches 1.. at @e[tag=rlk_body,limit=1] run tag @e[tag=rlk_mob,distance=..2.5] add rlk_llm
