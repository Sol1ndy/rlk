# @s = 스킬·폭발 피해를 받은 몹
execute store result score @s skEnd run time query gametime
scoreboard players operation @s skEnd += #skDur tmp
particle minecraft:dust{color:[0.65f,0.85f,0.29f],scale:0.9f} ~ ~2.1 ~ 0.15 0.1 0.15 0 6
