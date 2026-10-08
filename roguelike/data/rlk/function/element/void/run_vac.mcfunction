# 진공: 대상 잠식의 40% 를 주변 3칸의 다른 적에게 + 공허 부착, 바람 범위 피해
scoreboard players operation #g tmp = @s rnEr
scoreboard players operation #g tmp *= #c40 tmp
scoreboard players operation #g tmp /= #100 tmp
tag @s add rlk_rnc
execute if score #g tmp matches 1.. as @e[tag=rlk_mob,tag=!rlk_rnc,distance=..3] run function rlk:element/void/gain
tag @s remove rlk_rnc
particle minecraft:reverse_portal ~ ~1 ~ 1.2 0.5 1.2 0.4 60
particle minecraft:cloud ~ ~1 ~ 1 0.4 1 0.05 20
particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.1} ~ ~1 ~ 1.2 0.4 1.2 0 20
playsound minecraft:entity.breeze.inhale master @a ~ ~ ~ 0.8 0.8
playsound minecraft:entity.breeze.wind_burst master @a ~ ~ ~ 0.6 0.7
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,distance=..3] at @s run function rlk:element/aoe_hit
