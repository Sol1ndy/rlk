# Q pattern tick 88
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/p/q/lockp
execute if score #q_hit hr matches 1 at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run particle minecraft:dust{color:[1.0,0.95,0.98],scale:1.0} ~ ~ ~ 0.02 6 0.02 0 40 force @a[tag=player]
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run particle minecraft:dust{color:[0.88,0.25,0.62],scale:1.2} ~ ~ ~ 0.9 0.02 0.02 0 12 force @a[tag=player]
