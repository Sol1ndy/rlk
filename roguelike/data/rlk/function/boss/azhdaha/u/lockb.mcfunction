# The lock pulled into the body disc r 8 (a point the body moves to).
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_lock"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_lock,limit=1] run function rlk:boss/azhdaha/u/clamp_b
