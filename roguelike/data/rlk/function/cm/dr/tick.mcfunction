# 북잡이 (@s, at @s): 제자리. 북을 치는 동안(rlk_dr_drum) 10칸 안의 커스텀 몹이 빨라짐(cm/c2/world). 맞으면 2초 멈춤
scoreboard players set #hold tmp 1
execute if score @s c2T2 matches 1.. run return run function rlk:cm/dr/stopped
execute if score #free tmp matches 0 run return run tag @s remove rlk_dr_drum
tag @s add rlk_dr_drum
scoreboard players add @s c2T 1
execute if score @s c2T matches 16.. run scoreboard players set @s c2T 0
execute if score @s c2T matches 0 run function rlk:cm/dr/beat
execute if score @s c2T matches 8 run function rlk:cm/dr/beat
