# Minecraft display quaternion interpolation chooses the shortest return arc.
scoreboard players operation @s pmLocMode = @s pmWantMode
scoreboard players set @s pmLocT 0
scoreboard players set @s pmLocAcc 0
scoreboard players set @s pmBlend 6
execute if score @s pmWantMode matches 1.. run scoreboard players set @s pmBlend 4
execute store result storage rlk:player_motion loco.step int 1 run scoreboard players get @s pmBlend
function rlk:char/motion/loco/context
function rlk:char/motion/loco/pose with storage rlk:player_motion loco
function rlk:char/motion/loco/weapon
data modify storage rlk:player_motion loco.step set value 1
