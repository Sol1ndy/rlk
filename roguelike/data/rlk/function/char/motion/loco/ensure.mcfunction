function rlk:char/motion/loco/spawn with storage rlk:player_motion loco
scoreboard players set @s pmVisible 1
scoreboard players operation @s pmRigChar = #charN tmp
scoreboard players set @s pmLocMode -1
scoreboard players set @s pmWeapon -1
