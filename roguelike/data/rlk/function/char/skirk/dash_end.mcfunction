# 빠른 이동 끝: 스킬이 재사용 대기(#skDashCd)에 들어간다. 뱀의 계략은 남는다
scoreboard players set @s skDash 0
attribute @s minecraft:movement_speed modifier remove rlk:skirk_dash
execute unless score @s skM matches 1.. run attribute @s minecraft:knockback_resistance modifier remove rlk:skirk
scoreboard players operation @s skillCd = #skDashCd tmp
function rlk:char/skirk/cd_reduce
scoreboard players reset 빠른이동 stacks
# Only transition the hover animation; never replace a newly started attack or burst.
execute if score @s dead matches 1 run return 0
execute if score @s vMap matches 1 run return 0
execute if score @s pkMode matches 1.. run return 0
execute unless score @s pmActive matches 1 run function rlk:char/motion/start {char:"skirk",clip:"skill_right_end"}
execute if data storage rlk:player_motion active{char:"skirk",clip:"skill_right"} run function rlk:char/motion/start {char:"skirk",clip:"skill_right_end"}
execute if data storage rlk:player_motion active{char:"skirk",clip:"skill_right_loop"} run function rlk:char/motion/start {char:"skirk",clip:"skill_right_end"}
