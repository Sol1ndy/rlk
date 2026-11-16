# @s = 폭풍의 눈, at @s. 반경 6칸의 적(보스 제외)을 끌어당기고 0.4초마다 공격력의 40퍼센트 바람 원소 피해. 끝나면 원소 에너지를 돌려줌
scoreboard players remove @s life 1
particle minecraft:cloud ~ ~1.5 ~ 1.2 1.2 1.2 0.05 6
particle minecraft:dust{color:[0.44f,0.89f,0.76f],scale:1.5f} ~ ~1.5 ~ 2 1.4 2 0 12
execute as @e[tag=rlk_mob,tag=!boss,distance=0.9..6] at @s facing entity @e[tag=rlk_storm,limit=1,sort=nearest] feet rotated ~ 0 if block ^ ^ ^0.7 #rlk:view_pass if block ^ ^1 ^0.7 #rlk:view_pass run tp @s ^ ^ ^0.35
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #stormInt tmp
execute if score #t1 itv matches 0 if entity @e[tag=rlk_mob,distance=..5,limit=1] run function rlk:items/proc/storm_hit
execute if score @s life matches ..0 as @a[tag=player,limit=1] run function rlk:items/proc/storm_end
execute if score @s life matches ..0 run kill @s
