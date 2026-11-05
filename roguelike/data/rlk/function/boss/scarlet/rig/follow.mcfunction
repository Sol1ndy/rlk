# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).
execute store result score #x hrRigQ run data get entity @s Pos[0] 100
execute store result score #y hrRigQ run data get entity @s Pos[1] 100
execute store result score #z hrRigQ run data get entity @s Pos[2] 100
execute store result score #w hrRigQ run data get entity @s Rotation[0] 100
execute if score #x hrRigQ = @s hrRigQx if score #y hrRigQ = @s hrRigQy if score #z hrRigQ = @s hrRigQz if score #w hrRigQ = @s hrRigQw run return 0
scoreboard players operation @s hrRigQx = #x hrRigQ
scoreboard players operation @s hrRigQy = #y hrRigQ
scoreboard players operation @s hrRigQz = #z hrRigQ
scoreboard players operation @s hrRigQw = #w hrRigQ
function rlk:boss/scarlet/rig/follow/all
