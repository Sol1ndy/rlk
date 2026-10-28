# 졸개 (@s = 두뇌, at @s): 무리장 곁(2.5칸)에 붙어 다니고, 한 마리라도 2.5칸 안이면 무리 전체가 함께 칼을 든다(0.6초) → 짧은 베기
execute if score @s cmS matches 1 run return run function rlk:cm/ns/wind
execute if score @s cmAR matches 3.. run scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..2.5] run return run function rlk:cm/ns/pack_go
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/ns/cohere
