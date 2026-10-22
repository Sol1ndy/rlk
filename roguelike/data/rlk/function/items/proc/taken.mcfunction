# 받는 피해 감소 (@s = 플레이어, #dmgIn tmp): 선장의 팔보호대(개수당 #bracerRes‰) + 불사자의 갈기(#lionRes‰). 합쳐서 최대 60%(600‰)
scoreboard players operation #t1 itv = @s it_captain_bracer
scoreboard players operation #t1 itv *= #bracerRes tmp
execute if score @s it_lion_mane matches 1.. run scoreboard players operation #t1 itv += #lionRes tmp
execute if score #t1 itv matches ..0 run return 0
execute if score #t1 itv matches 601.. run scoreboard players set #t1 itv 600
scoreboard players set #t2 itv 1000
scoreboard players operation #t2 itv -= #t1 itv
scoreboard players operation #dmgIn tmp *= #t2 itv
scoreboard players operation #dmgIn tmp /= #1000 tmp
execute if score #dmgIn tmp matches ..0 run scoreboard players set #dmgIn tmp 1
