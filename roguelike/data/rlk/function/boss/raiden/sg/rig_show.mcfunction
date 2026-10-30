# core tick: the first visible tick after a hide. A clip queued this tick shows the rig; otherwise the idle.
execute unless score @s rdRigT matches -1 run function rlk:boss/raiden/sg/idle_clip
scoreboard players set @s rdHidden 0
