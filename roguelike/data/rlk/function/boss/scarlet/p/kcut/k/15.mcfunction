# KCUT pattern tick 15
function rlk:boss/scarlet/p/kcut/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..7] rotated as @s rotated ~ 0 positioned ^ ^ ^7 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
