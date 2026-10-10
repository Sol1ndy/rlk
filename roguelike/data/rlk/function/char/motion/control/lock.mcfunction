# Short authored action lock; dash and other attacks can cancel ordinary swings.
scoreboard players set @s pmMoveLock 1
scoreboard players set @s stepT 0
scoreboard players set @s dashMoveT 0
attribute @s minecraft:movement_speed modifier remove rlk:motion_hold
attribute @s minecraft:movement_speed modifier add rlk:motion_hold -1 add_multiplied_total
attribute @s minecraft:jump_strength modifier remove rlk:motion_hold
attribute @s minecraft:jump_strength modifier add rlk:motion_hold -1 add_multiplied_total
function rlk:view/stop_h
