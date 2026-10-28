# 번개 슬라임 (@s, at @s): 몸 쪽으로 깡충 뛰어 옴. 3.2칸 안이면 0.5초 웅크림(예고) → 몸통 박치기(12, 번개)
execute if score @s cmS matches 1 run return run function rlk:cm/sl/crouch
execute if score @s cmS matches 2 run return run function rlk:cm/sl/air
scoreboard players remove @s c2T 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s c2T 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..3.2] run return run function rlk:cm/sl/start
execute if score #free tmp matches 1 if score @s c2T matches ..0 run function rlk:cm/sl/hop
