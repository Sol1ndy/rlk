# @s turns (yaw only) toward the player's body at once.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
