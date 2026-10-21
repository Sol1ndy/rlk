# @s = body: the hit disc onto the body front; its first touch (hit or dash) shows the contact impact once.
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^2.5 as @e[type=minecraft:marker,tag=rlk_mb_az_p3h] run tp @s ~ ~ ~ ~ 0
execute unless score #aq3X mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_p3h] if score @s mbHzHit matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:mboss/azhdaha/p/charge/contact
