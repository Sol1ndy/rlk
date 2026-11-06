# A crab-turn step toward the player: turn_p1_step (-90 deg) mirrored when the player is on the right.
function rlk:mboss/mv/local
scoreboard players set #apYawS mb 1
execute if score #mbLs mb matches ..-1 run scoreboard players set #apYawS mb -1
function rlk:boss/apep/play/turn_p1_step
