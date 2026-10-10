execute if score @s dead matches 1 run return run function rlk:char/skirk/dash_end
execute if score @s vMap matches 1 run return run function rlk:char/skirk/dash_end
execute if score @s pkMode matches 1.. run return run function rlk:char/skirk/dash_end
# 빠른 이동 중 (@s = 플레이어, at 몸): 주변의 허계 균열을 흡수
scoreboard players remove @s skDash 1
execute if entity @e[tag=rlk_rift,distance=..6] run function rlk:char/skirk/absorb
scoreboard players operation #lp tmp = @s skDash
scoreboard players add #lp tmp 19
scoreboard players operation #lp tmp /= #st20 tmp
scoreboard players operation 빠른이동 stacks = #lp tmp
scoreboard players display name 빠른이동 stacks {text:"빠른 이동",color:"#9FE8F5"}
execute if score @s skDash matches ..0 run function rlk:char/skirk/dash_end

execute if score @s skDash matches 1.. unless score @s pmActive matches 1 run function rlk:char/motion/start {char:"skirk",clip:"skill_right_loop"}
