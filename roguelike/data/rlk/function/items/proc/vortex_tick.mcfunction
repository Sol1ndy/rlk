# @s = 회오리, at @s. 반경 5칸의 적(보스 제외)을 틱마다 0.3칸씩 끌어당기고, 0.5초마다 공격력의 20퍼센트 바람 원소 피해
scoreboard players remove @s life 1
particle minecraft:cloud ~ ~1 ~ 0.8 0.6 0.8 0.02 3
particle minecraft:dust{color:[0.44f,0.89f,0.76f],scale:1.2f} ~ ~1 ~ 1.5 0.8 1.5 0 6
execute as @e[tag=rlk_mob,tag=!boss,distance=0.9..5] at @s facing entity @e[tag=rlk_vortex,limit=1,sort=nearest] feet rotated ~ 0 if block ^ ^ ^0.7 #rlk:view_pass if block ^ ^1 ^0.7 #rlk:view_pass run tp @s ^ ^ ^0.3
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st10 tmp
execute if score #t1 itv matches 0 if entity @e[tag=rlk_mob,distance=..5,limit=1] run function rlk:items/proc/vortex_hit
execute if score @s life matches ..0 run kill @s
