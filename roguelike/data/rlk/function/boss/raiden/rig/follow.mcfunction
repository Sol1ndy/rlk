# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).
execute store result score #x rdRigQ run data get entity @s Pos[0] 100
execute store result score #y rdRigQ run data get entity @s Pos[1] 100
execute store result score #z rdRigQ run data get entity @s Pos[2] 100
execute store result score #w rdRigQ run data get entity @s Rotation[0] 100
execute if score #x rdRigQ = @s rdRigQx if score #y rdRigQ = @s rdRigQy if score #z rdRigQ = @s rdRigQz if score #w rdRigQ = @s rdRigQw run return 0
scoreboard players operation @s rdRigQx = #x rdRigQ
scoreboard players operation @s rdRigQy = #y rdRigQ
scoreboard players operation @s rdRigQz = #z rdRigQ
scoreboard players operation @s rdRigQw = #w rdRigQ
execute if score @s rdRigFl matches 1 run return run function rlk:boss/raiden/rig/follow/tenma
execute if score @s rdRigFl matches 2 run return run function rlk:boss/raiden/rig/follow/all
function rlk:boss/raiden/rig/follow/shogun
