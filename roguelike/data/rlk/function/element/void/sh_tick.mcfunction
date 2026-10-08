# 날아가는 파편 (@s = 파편, at @s): 4틱 동안 밖으로, 그 뒤 맞힐 몹 쪽으로 휘어 들어간다. 2초가 지나거나 몹이 사라지면 부서짐
scoreboard players add @s life 1
execute if score @s life matches 40.. run return run function rlk:element/void/sh_fizz
scoreboard players operation #tg tmp = @s rnTg
execute as @e[tag=rlk_mob] if score @s rnId = #tg tmp run tag @s add rlk_rntgt
execute unless entity @e[tag=rlk_rntgt,limit=1] run return run function rlk:element/void/sh_fizz
execute if score @s life matches ..4 run tp @s ^ ^ ^0.5
execute if score @s life matches 5..11 positioned ^ ^ ^1 facing entity @e[tag=rlk_rntgt,limit=1] eyes positioned ^ ^ ^1.6 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_aimpt"]}
execute if score @s life matches 12.. facing entity @e[tag=rlk_rntgt,limit=1] eyes positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_aimpt"]}
execute if score @s life matches 5.. facing entity @e[tag=rlk_aimpt,limit=1] feet run tp @s ~ ~ ~ ~ ~
kill @e[tag=rlk_aimpt]
execute if score @s life matches 5.. at @s run tp @s ^ ^ ^0.8
execute at @s run particle minecraft:snowflake ~ ~ ~ 0.03 0.03 0.03 0 1
execute at @s run particle minecraft:dust{color:[0.75,0.93,1.0],scale:0.6} ~ ~ ~ 0 0 0 0 1
execute at @s positioned ~-0.7 ~-0.7 ~-0.7 if entity @e[tag=rlk_rntgt,dx=0.4,dy=0.4,dz=0.4] run function rlk:element/void/sh_hit
tag @e[tag=rlk_rntgt] remove rlk_rntgt
