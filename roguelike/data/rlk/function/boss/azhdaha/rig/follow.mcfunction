# Parts (and the shadow helper) follow the anchor position and yaw (run as and rotated as the anchor, pitch 0); the list is the body state's (azRigFl: 0 all, 1 tail, 2 none), skipped while the anchor stands still.
execute store result score #x azRigQ run data get entity @s Pos[0] 100
execute store result score #y azRigQ run data get entity @s Pos[1] 100
execute store result score #z azRigQ run data get entity @s Pos[2] 100
execute store result score #w azRigQ run data get entity @s Rotation[0] 100
execute if score #x azRigQ = @s azRigQx if score #y azRigQ = @s azRigQy if score #z azRigQ = @s azRigQz if score #w azRigQ = @s azRigQw run return 0
scoreboard players operation @s azRigQx = #x azRigQ
scoreboard players operation @s azRigQy = #y azRigQ
scoreboard players operation @s azRigQz = #z azRigQ
scoreboard players operation @s azRigQw = #w azRigQ
execute if score @s azRigFl matches 1 run return run function rlk:boss/azhdaha/rig/follow/tail
execute if score @s azRigFl matches 2 run return run function rlk:boss/azhdaha/rig/follow/none
function rlk:boss/azhdaha/rig/follow/all
