# End the old action while preserving all display transforms for interpolation.
execute if score @s pmActive matches 1 run function rlk:char/motion/control/cancel
execute if data storage rlk:player_motion active.clip run function rlk:char/motion/audio/stop with storage rlk:player_motion active
function rlk:char/motion/control/unlock
scoreboard players set @s pmActive 0
scoreboard players set @s pmTick 0
scoreboard players set @s pmAcc 0
scoreboard players set @s pmAtkPending 0
kill @e[tag=rlk_pm_basis]
data remove storage rlk:player_motion active
