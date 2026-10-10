# 쉬는 동안(사망·아이템 선택 공간): 달리기 시야 효과만 풀어 둠 · F5 위쪽 시점이면 내리고 원래 크기로
execute if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/ride_off
execute if score #spr view matches 1 run attribute @s minecraft:movement_speed modifier remove rlk:view_sprint
scoreboard players set #spr view 0
