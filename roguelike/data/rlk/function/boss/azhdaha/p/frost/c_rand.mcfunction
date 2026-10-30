# @s = body: a centre 8-20 b from the tail (the anchor) in a random direction.
summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p41","rlk_mb_az_p41c"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359
execute store result storage rlk:mboss az.p41.d int 1 run random value 8..20
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] at @s rotated as @s run function rlk:boss/azhdaha/p/frost/mv with storage rlk:mboss az.p41
