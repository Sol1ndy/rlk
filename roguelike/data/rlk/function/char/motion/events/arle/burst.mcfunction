function rlk:char/motion/audio/arle/burst
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 60
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 0 run scoreboard players set #pmInv tmp 60
execute if score @s pmTick matches 0 run scoreboard players operation @s dashInvT > #pmInv tmp
