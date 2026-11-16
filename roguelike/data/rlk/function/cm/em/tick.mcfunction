# 단검 용병 (@s, at @s): 9칸 밖이면 걸어 옴. 안이면 무리가 몸 둘레 4칸을 함께 돎(자리 = 무리 각도). 둘씩 0.6초 웅크림 → 몸 쪽으로 돌진 찌르기(14), 가운데서 뭉친 채 0.8초 멈춤
execute if score @s cmS matches 1 run return run function rlk:cm/em/crouch
execute if score @s cmS matches 2 run return run function rlk:cm/em/dash
execute if score @s cmAR matches 1.. run return run scoreboard players set #hold tmp 1
execute unless entity @e[tag=rlk_body,distance=..9] run return 0
scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..6.5] run return run function rlk:cm/em/pair_go
execute if score #free tmp matches 0 run return 0
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/em/orbit
