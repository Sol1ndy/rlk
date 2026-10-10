execute if data storage rlk:player_motion active{lockedYaw:1b} unless entity @e[tag=rlk_pm_basis,limit=1] run return run function rlk:char/motion/finish
execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/respawn with storage rlk:player_motion active
execute if entity @e[tag=rlk_pm] run scoreboard players set @s pmVisible 1
execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar
execute unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
execute if data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
scoreboard players operation @s pmAcc += @s pmSpeed
execute if score @s pmAcc matches 100.. unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/advance
execute if score @s pmAcc matches 100.. if data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run function rlk:char/motion/advance
