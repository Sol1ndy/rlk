# 바닐라 체력을 1024로 고정(피해 감지용). 실제 체력은 mhpC / mhpM
attribute @s minecraft:max_health base set 1024
data modify entity @s Health set value 1024f
