# @s = a new hazard without an explicit #hzNoParry (combat overhaul C, the user's 11-10 choice: only some big boss attacks are
# unparriable - area attacks and grabs). Unparriable by default: no-dodge (#hzNoDodge), per mille (#hzPm), re-arming
# (#hzRearm: a lingering field), ring (a wave), full arena, mask; a disc of radius >= 4.5 b; a sector or a line reaching
# >= 8 b. Parryable: the smaller one-shot disc / sector / line (the weapon strikes, sword-qi), and every projectile.
scoreboard players set @s mbHzNP 1
execute if score @s mbHzND matches 1 run return 0
execute if score @s mbHzPm matches 1.. run return 0
execute if score @s mbHzRA matches 1.. run return 0
execute if score @s mbHzK matches 1 if score @s mbHzR matches ..4499 run return run scoreboard players set @s mbHzNP 0
execute if score @s mbHzK matches 3..4 if score @s mbHzR matches ..7999 run return run scoreboard players set @s mbHzNP 0
