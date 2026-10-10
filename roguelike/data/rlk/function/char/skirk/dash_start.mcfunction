# 빠른 이동 시작: 1인칭 = 이동 속도 1.5배(수정자), 숄더뷰 = view/move 에서 #skDashSpd%
scoreboard players operation @s skDash = #skDashDur tmp
attribute @s minecraft:movement_speed modifier add rlk:skirk_dash 0.5 add_multiplied_total
attribute @s minecraft:knockback_resistance modifier add rlk:skirk 1 add_value
function rlk:char/motion/start {char:"skirk",clip:"skill_right"}
