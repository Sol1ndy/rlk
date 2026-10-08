# @s = 플레이어, at @s. 뇌벌 악요의 눈이 머리 위에 떠서 따라다님 (살짝 오르내림, 빛줄기는 천천히 맥동)
kill @e[tag=rlk_eye,tag=!rlk_eyev]
execute unless entity @e[tag=rlk_eyev,limit=1] positioned ~ ~2.85 ~ run function rlk:items/proc/eye_parts
scoreboard players add @s eyeAnim 1
execute if score @s eyeAnim matches 80.. run scoreboard players set @s eyeAnim 0
execute if score @s eyeAnim matches 0..19 run tp @e[tag=rlk_eyev] ~ ~2.85 ~
execute if score @s eyeAnim matches 20..39 run tp @e[tag=rlk_eyev] ~ ~2.91 ~
execute if score @s eyeAnim matches 40..59 run tp @e[tag=rlk_eyev] ~ ~2.85 ~
execute if score @s eyeAnim matches 60..79 run tp @e[tag=rlk_eyev] ~ ~2.79 ~
# 반짝임(과하지 않게): 0.4초마다 흰 별빛(wax_off, 1~2초 남아 흩어짐) 하나, 0.8초마다 보랏빛 반짝임(witch) 하나
scoreboard players operation #ea tmp = @s eyeAnim
scoreboard players operation #ea tmp %= #st8 tmp
execute if score #ea tmp matches 0 run particle minecraft:wax_off ~ ~2.85 ~ 0.4 0.12 0.4 1.5 1
scoreboard players operation #ea tmp = @s eyeAnim
scoreboard players operation #ea tmp %= #st16 tmp
execute if score #ea tmp matches 4 run particle minecraft:witch ~ ~2.8 ~ 0.4 0.1 0.4 0 1
execute if score @s eyeAnim matches 0 run data merge entity @e[tag=rlk_eye_s0,limit=1] {start_interpolation:0,interpolation_duration:40,transformation:{translation:[0.0000f,-0.0780f,0.0000f],left_rotation:[0f,0f,0.00000f,1.00000f],scale:[1.8243f,0.1103f,0.0020f],right_rotation:[0f,0f,0.38268f,0.92388f]}}
execute if score @s eyeAnim matches 0 run data merge entity @e[tag=rlk_eye_s1,limit=1] {start_interpolation:0,interpolation_duration:40,transformation:{translation:[0.0000f,-0.0255f,0.0040f],left_rotation:[0f,0f,0.00000f,1.00000f],scale:[1.6122f,0.0361f,0.0020f],right_rotation:[0f,0f,0.38268f,0.92388f]}}
execute if score @s eyeAnim matches 40 run data merge entity @e[tag=rlk_eye_s0,limit=1] {start_interpolation:0,interpolation_duration:40,transformation:{translation:[0.0000f,-0.0660f,0.0000f],left_rotation:[0f,0f,0.00000f,1.00000f],scale:[1.5274f,0.0933f,0.0020f],right_rotation:[0f,0f,0.38268f,0.92388f]}}
execute if score @s eyeAnim matches 40 run data merge entity @e[tag=rlk_eye_s1,limit=1] {start_interpolation:0,interpolation_duration:40,transformation:{translation:[0.0000f,-0.0225f,0.0040f],left_rotation:[0f,0f,0.00000f,1.00000f],scale:[1.3152f,0.0318f,0.0020f],right_rotation:[0f,0f,0.38268f,0.92388f]}}
