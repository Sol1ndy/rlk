# @s = 치유받는 두뇌, at @s
scoreboard players operation #c3hv tmp = @s mhpM
scoreboard players operation #c3hv tmp *= #c3Hp_cw tmp
scoreboard players operation #c3hv tmp /= #c2c100 tmp
execute if score #c3hv tmp matches ..0 run scoreboard players set #c3hv tmp 1
scoreboard players operation @s mhpC += #c3hv tmp
scoreboard players operation @s mhpC < @s mhpM
particle minecraft:splash ~ ~1 ~ 0.3 0.4 0.3 0.1 12 normal
particle minecraft:dust{color:[0.45,0.8,1.0],scale:1.2} ~ ~1.1 ~ 0.3 0.4 0.3 0 6 normal
scoreboard players set #c3rs tmp 16
execute positioned ~ ~1.1 ~ facing entity @e[tag=rlk_c3heal,limit=1] feet positioned ^ ^ ^0.5 run function rlk:cm/cw/ribbon
