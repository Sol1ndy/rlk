# The lock of the next disc (7 t before its release; @s = the body): a marker at the player's feet on the floor
# (rlk_hr_lock + the pattern tags, as p1's lock_fn), she faces it from now on; g/disc/throw aims at it and removes it.
kill @e[type=minecraft:marker,tag=rlk_hr_lock]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_lock","rlk_hr_gln"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_gln] run function rlk:boss/scarlet/g/disc/tag
tag @e[type=minecraft:marker,tag=rlk_hr_gln] remove rlk_hr_gln
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
