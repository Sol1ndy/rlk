# Minecraft display quaternion interpolation chooses the shortest return arc.
scoreboard players operation @s pmLocMode = @s pmWantMode
scoreboard players set @s pmLocT 0
scoreboard players set @s pmLocAcc 0
scoreboard players set @s pmLocS 0
execute if score @s pmSheath matches 1 run scoreboard players set @s pmLocS 1
scoreboard players set @s pmBlend 6
execute if score @s pmWantMode matches 1.. run scoreboard players set @s pmBlend 4
execute store result storage rlk:player_motion loco.step int 1 run scoreboard players get @s pmBlend
function rlk:char/motion/loco/context
function rlk:char/motion/loco/pose with storage rlk:player_motion loco
# Hand and back never blend into each other: the weapon snaps when the attach changes.
execute unless score @s pmWAt = @s pmLocS run function rlk:char/motion/sheath/snap
scoreboard players operation @s pmWAt = @s pmLocS
function rlk:char/motion/loco/weapon
data modify storage rlk:player_motion loco.step set value 1
