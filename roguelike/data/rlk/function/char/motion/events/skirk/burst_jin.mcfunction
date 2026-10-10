function rlk:char/motion/audio/skirk/burst_jin
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 20
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 0 run scoreboard players set #pmInv tmp 20
execute if score @s pmTick matches 0 run scoreboard players operation @s dashInvT > #pmInv tmp
execute if score @s pmTick matches 10 if score @s skM matches 1.. run function rlk:char/skirk/ruin_apply
