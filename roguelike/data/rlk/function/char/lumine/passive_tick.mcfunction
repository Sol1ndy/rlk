scoreboard players remove @s lumP 1
scoreboard players operation #lp tmp = @s lumP
scoreboard players add #lp tmp 19
scoreboard players operation #lp tmp /= #st20 tmp
scoreboard players operation 예리한얼음 stacks = #lp tmp
scoreboard players display name 예리한얼음 stacks {text:"예리한 얼음",color:"#9FE8FF"}
execute if score @s lumP matches 0 run scoreboard players reset 예리한얼음 stacks
scoreboard players operation #lp tmp = @s lumP
scoreboard players operation #lp tmp %= #st4 tmp
execute if score #lp tmp matches 0 positioned ~ ~1.62 ~ run particle minecraft:snowflake ^-0.35 ^-0.45 ^0.6 0.08 0.12 0.08 0.01 1
