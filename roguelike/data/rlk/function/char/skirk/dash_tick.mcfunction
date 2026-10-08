# 빠른 이동 중 (@s = 플레이어, at 몸): 주변의 허계 균열을 흡수
scoreboard players remove @s skDash 1
execute if entity @e[tag=rlk_rift,distance=..6] run function rlk:char/skirk/absorb
particle minecraft:snowflake ~ ~0.6 ~ 0.2 0.4 0.2 0.01 2
particle minecraft:reverse_portal ~ ~0.8 ~ 0.2 0.4 0.2 0.02 2
scoreboard players operation #lp tmp = @s skDash
scoreboard players add #lp tmp 19
scoreboard players operation #lp tmp /= #st20 tmp
scoreboard players operation 빠른이동 stacks = #lp tmp
scoreboard players display name 빠른이동 stacks {text:"빠른 이동",color:"#9FE8F5"}
execute if score @s skDash matches ..0 run function rlk:char/skirk/dash_end
