# Called once for each authored tick, including intermediate frames at high attack speed.
function rlk:char/motion/event_dispatch with storage rlk:player_motion active
execute if score @s pmMoveLock matches 1 if score @s pmTick >= @s pmLockUntil run function rlk:char/motion/control/unlock
execute if score @s pmAtkPending matches 1 if score @s pmTick >= @s pmStrike run function rlk:char/motion/combat/first
execute if score @s pmAtkPending matches 2 if score @s pmTick >= @s pmSecond run function rlk:char/motion/combat/second
