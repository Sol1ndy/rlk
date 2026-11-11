# Cancel the running pattern, no recovery (A6 interrupts a windup, the groggy; @s = body).
function rlk:boss/scarlet/core/cancel_d
scoreboard players set #pat hr 0
scoreboard players set #done hr 0
scoreboard players set #pt hr 0
scoreboard players set #ppf hr 0
scoreboard players set #ultq hr 0
function rlk:boss/scarlet/core/stop_move
kill @e[type=minecraft:marker,tag=rlk_hr_lock]
function rlk:boss/scarlet/core/ground
