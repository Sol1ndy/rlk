# @s = the anchor: one 0.1-b step of the player's body toward the front exit, while #pN steps are left.
execute unless score #pN mb matches 1.. run return 0
scoreboard players remove #pN mb 1
scoreboard players set #pkbBlocked tmp 0
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^0.1 run function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 1 run return 0
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^0.1 run tp @e[tag=rlk_body,limit=1] ~ ~ ~
function rlk:mboss/push/step_front
