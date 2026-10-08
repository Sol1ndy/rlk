# 바닐라 체력을 상한으로 늘리고 가득 채움 (@s = 플레이어)
attribute @s minecraft:max_health base set 1024
effect give @s minecraft:instant_health 1 20 true
scoreboard players set @s vhp 1024
