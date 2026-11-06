# @s = body (t1): the landing point (plan 5 P2): from the anchor toward the player's feet, travel
# clamp(dist - 3, 4, 14) b (0.5-b steps), then pulled into the body disc r 8.
kill @e[type=minecraft:marker,tag=rlk_mb_az_p2l]
summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p2","rlk_mb_az_p2l"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^4 ~ 0
scoreboard players set #aq2N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] at @s run function rlk:boss/azhdaha/p/jump/lstep
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] run function rlk:boss/azhdaha/u/clamp_b
