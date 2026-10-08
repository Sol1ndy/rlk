# 빠른 이동 시작: 1인칭 = 이동 속도 2배(수정자), 숄더뷰 = view/move 에서 #skDashSpd%
scoreboard players operation @s skDash = #skDashDur tmp
attribute @s minecraft:movement_speed modifier add rlk:skirk_dash 1.0 add_multiplied_total
attribute @s minecraft:knockback_resistance modifier add rlk:skirk 1 add_value
playsound minecraft:entity.breeze.charge master @a ~ ~ ~ 0.7 1.6
playsound minecraft:item.trident.riptide_1 master @a ~ ~ ~ 0.5 1.6
particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.6 0.4 0.08 30
