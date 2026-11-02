# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).
execute store result score #x knRigQ run data get entity @s Pos[0] 100
execute store result score #y knRigQ run data get entity @s Pos[1] 100
execute store result score #z knRigQ run data get entity @s Pos[2] 100
execute store result score #w knRigQ run data get entity @s Rotation[0] 100
execute if score #x knRigQ = @s knRigQx if score #y knRigQ = @s knRigQy if score #z knRigQ = @s knRigQz if score #w knRigQ = @s knRigQw run return 0
scoreboard players operation @s knRigQx = #x knRigQ
scoreboard players operation @s knRigQy = #y knRigQ
scoreboard players operation @s knRigQz = #z knRigQ
scoreboard players operation @s knRigQw = #w knRigQ
execute if score @s knRigFl matches 1 run return run function rlk:boss/arlecchino/rig/follow/no_r
execute if score @s knRigFl matches 2 run return run function rlk:boss/arlecchino/rig/follow/no_l
execute if score @s knRigFl matches 3 run return run function rlk:boss/arlecchino/rig/follow/no_rl
function rlk:boss/arlecchino/rig/follow/all
