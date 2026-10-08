# 쉬는 동안(사망·아이템 선택 공간): 달리기 시야 효과만 풀어 둠
execute if score #spr view matches 1 run attribute @s minecraft:movement_speed modifier remove rlk:view_sprint
scoreboard players set #spr view 0
