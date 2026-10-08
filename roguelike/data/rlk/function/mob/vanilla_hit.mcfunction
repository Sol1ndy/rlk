# @s = 몹. 바닐라 피해(낙하·불·다른 몹 등)를 받음: 깎인 만큼(올림) 실제 체력에서 빼고 바닐라 체력을 다시 채움. #vh tmp = 바닐라 체력 × 100
scoreboard players set #vd tmp 102400
scoreboard players operation #vd tmp -= #vh tmp
scoreboard players add #vd tmp 99
scoreboard players operation #vd tmp /= #100 tmp
scoreboard players operation @s mhpC -= #vd tmp
execute if score @s mhpC matches ..0 run return run kill @s
data modify entity @s Health set value 1024f
