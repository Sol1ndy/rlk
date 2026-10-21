# @s = body (t38, still hidden, 4 t before it shows): the facing f = from L toward the player (along the
# hidden path when the player stands on L); the anchor goes to L - 2.59 f (the clip's burst point lands on L),
# the roll end E = L + 1.41 f (clamped to r 16), the slam point S = E -1.16 f.
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet run tp @s ~ ~ ~ ~180 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] at @s unless entity @e[tag=rlk_body,distance=..1,limit=1] facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p31e]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p31s]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] positioned ^ ^ ^1.41 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p31","rlk_mb_ap_p31e"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p31e,limit=1] at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p31e,limit=1] run function rlk:boss/apep/u/clamp_glide
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p31e,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] positioned ^ ^ ^-1.16 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p31","rlk_mb_ap_p31s"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] positioned ^ ^ ^-2.59 run tp @s ~ 201 ~ ~ 0
# TODO(I2): Gen.yaw_rebase() (RP3-1): the yaw driver holds the new facing (the schedule is 0 until t66)
execute store result score #apYaw0 mb run data get entity @s Rotation[0] 100
