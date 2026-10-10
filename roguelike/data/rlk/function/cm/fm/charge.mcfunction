scoreboard players set #hold tmp 1
scoreboard players remove @s cmT 1
# n번째 화염구: 남은 차지 ≤ 차지 × (4 - n) / 3 - 2
scoreboard players set #th tmp 3
scoreboard players operation #th tmp -= @s cmN
scoreboard players operation #th tmp *= #cmW_fm tmp
scoreboard players operation #th tmp /= #3 tmp
scoreboard players remove #th tmp 2
execute if score @s cmN matches ..2 if score @s cmT <= #th tmp run function rlk:cm/fm/ball_next
particle minecraft:flame ~ ~1.1 ~ 0.35 0.6 0.35 0.01 2
function rlk:cm/fm/hold
execute if score @s cmT matches ..0 run function rlk:cm/fm/vstart
