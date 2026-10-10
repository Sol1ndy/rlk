# @s = 회오리, at @s. 0.5초마다 반경 5칸의 적에게 공격력의 20퍼센트 바람 원소 피해
scoreboard players remove @s life 1
particle minecraft:cloud ~ ~1 ~ 0.8 0.6 0.8 0.02 3
particle minecraft:dust{color:[0.44f,0.89f,0.76f],scale:1.2f} ~ ~1 ~ 1.5 0.8 1.5 0 6
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st10 tmp
execute if score #t1 itv matches 0 if entity @e[tag=rlk_mob,distance=..5,limit=1] run function rlk:items/proc/vortex_hit
execute if score @s life matches ..0 run kill @s
