# A9 pattern tick 21
function rlk:boss/scarlet/p/a9/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..9] rotated as @s rotated ~ 0 positioned ^ ^ ^9 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
