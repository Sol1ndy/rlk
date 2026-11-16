# @s = body, #azB3T = a circle tick. The centre: 70 % at the player (lockv lead 15, then 2 b along the velocity,
# or 4 b off a standing player in a random direction), 30 % random 8-20 b from the tail; nudged off live fields
# and orbit bands, kept in the walk disc; then drawn and armed (plan 5 41).
kill @e[type=minecraft:marker,tag=rlk_mb_az_p41c]
execute store result score #aq41R mb run random value 0..99
execute if score #aq41R mb matches ..69 run function rlk:boss/azhdaha/p/frost/c_pl
execute if score #aq41R mb matches 70.. run function rlk:boss/azhdaha/p/frost/c_rand
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] at @s run function rlk:boss/azhdaha/p/frost/nudge
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] run function rlk:boss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] run function rlk:boss/azhdaha/p/frost/make
