# 일곱빛 섬광 중 (@s = 플레이어, at 몸): 뱀의 계략이 줄어든다. 다 떨어지거나 시간이 끝나면 종료
scoreboard players remove @s skM 1
scoreboard players operation @s energy -= #skDrain tmp
execute if score @s energy matches ..0 run return run function rlk:char/skirk/mode_end
execute if score @s skM matches ..0 run return run function rlk:char/skirk/mode_end
scoreboard players operation #lp tmp = @s skM
scoreboard players add #lp tmp 19
scoreboard players operation #lp tmp /= #st20 tmp
scoreboard players operation 일곱빛섬광 stacks = #lp tmp
scoreboard players display name 일곱빛섬광 stacks {text:"일곱빛 섬광",color:"#9FE8F5"}
scoreboard players operation #lp tmp = @s skM
scoreboard players operation #lp tmp %= #st4 tmp
execute if score #lp tmp matches 0 run particle minecraft:snowflake ~ ~0.9 ~ 0.35 0.5 0.35 0.01 2
execute if score #lp tmp matches 0 run particle minecraft:reverse_portal ~ ~0.9 ~ 0.3 0.5 0.3 0.01 1
