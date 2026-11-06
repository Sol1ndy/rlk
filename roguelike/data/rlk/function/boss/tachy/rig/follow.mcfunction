# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).
execute store result score #x tkRigQ run data get entity @s Pos[0] 100
execute store result score #y tkRigQ run data get entity @s Pos[1] 100
execute store result score #z tkRigQ run data get entity @s Pos[2] 100
execute store result score #w tkRigQ run data get entity @s Rotation[0] 100
execute if score #x tkRigQ = @s tkRigQx if score #y tkRigQ = @s tkRigQy if score #z tkRigQ = @s tkRigQz if score #w tkRigQ = @s tkRigQw run return 0
scoreboard players operation @s tkRigQx = #x tkRigQ
scoreboard players operation @s tkRigQy = #y tkRigQ
scoreboard players operation @s tkRigQz = #z tkRigQ
scoreboard players operation @s tkRigQw = #w tkRigQ
function rlk:boss/tachy/rig/follow/all
