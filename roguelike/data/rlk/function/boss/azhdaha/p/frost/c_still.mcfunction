# @s = the centre: a standing player gets the circle 4 b off them in a random direction.
execute store result entity @s Rotation[0] float 1 run random value 0..359
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @s rotated ~ 0 run tp @s ^ ^ ^4
