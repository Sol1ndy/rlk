# 창병 (@s, at @s): 초당 90°로만 돌아섬. 앞(±45°) 4.2칸 안이면 대열 전체가 1초 창끝 빛 → 2칸 찌르며 돌진(16)
execute if score @s cmS matches 1 run return run function rlk:cm/sp/wind
execute if score @s cmS matches 2 run return run function rlk:cm/sp/thrust
function rlk:cm/sp/turn
execute if score @s cmAR matches 1.. run scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if score @s cmAR matches ..0 if score #c2yd tmp matches -4500..4500 if entity @e[tag=rlk_body,distance=..4.2] run return run function rlk:cm/sp/line_go
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/sp/form
