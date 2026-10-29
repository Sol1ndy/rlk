# 둥실 버섯 (@s = 두뇌, at @s): 무리장 곁(1.8칸)에 뭉쳐 떠다니며 다가옴. 2.4칸 안이면 0.5초 부풀기(예고) → 몸통 박치기(10)
execute if score @s cmS matches 1 run return run function rlk:cm/fu/swell
execute if score @s cmS matches 2 run return run function rlk:cm/fu/bump
execute if score @s cmAR matches 1.. run scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..2.4] run return run function rlk:cm/fu/start
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/fu/cohere
