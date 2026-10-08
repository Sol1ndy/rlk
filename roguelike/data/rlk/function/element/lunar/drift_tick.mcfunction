# 월광 결정 (@s, at @s): 천천히 돌고, 1.5초마다 가까운 적에게 빛줄기
scoreboard players remove @s life 1
execute if score @s life matches ..0 run return run kill @s
tp @s ~ ~ ~ ~6 ~
particle minecraft:end_rod ~ ~ ~ 0.15 0.15 0.15 0 1
scoreboard players remove @s lnI 1
execute if score @s lnI matches 1.. run return 0
scoreboard players set @s lnI 30
execute unless entity @e[tag=rlk_mob,distance=..6] run return 0
scoreboard players operation #lnB tmp = @s rxDmg
tag @e[tag=rlk_mob,distance=..6,sort=nearest,limit=1] add rlk_lnt
scoreboard players set #sn tmp 0
execute facing entity @e[tag=rlk_lnt,limit=1] eyes run function rlk:element/lunar/drift_beam
execute as @e[tag=rlk_lnt] at @s run function rlk:element/lunar/drift_hit
tag @e[tag=rlk_lnt] remove rlk_lnt
