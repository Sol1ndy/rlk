# 풀차지 뒤에도 계속 당기고 있으면 #yoiKGap 틱마다 염초 화살이 하나씩(최대 3) 생긴다. 염초 정화의 춤 지속 중에는 생기지 않는다
execute if score @s yoiSk matches 1.. run return 0
execute if score @s bowK matches 3.. run return 0
scoreboard players operation #th tmp = @s bowK
scoreboard players add #th tmp 1
scoreboard players operation #th tmp *= #yoiKGap tmp
scoreboard players operation #th tmp += #bowT1 tmp
execute if score #ct tmp < #th tmp run return 0
scoreboard players add @s bowK 1
scoreboard players operation 염초화살 stacks = @s bowK
scoreboard players display name 염초화살 stacks {text:"염초 화살",color:"#FF8A3D"}
execute unless score #k244 snd matches 1 run function rlk:snd/f271
execute unless score #k245 snd matches 1 run function rlk:snd/f272
particle minecraft:flame ~ ~1.9 ~ 0.3 0.1 0.3 0.02 6
