# Parts and the shadow helper follow the anchor (run as and rotated as the anchor at its feet, pitch 0).
execute store result score #x apRigQ run data get entity @s Pos[0] 100
execute store result score #y apRigQ run data get entity @s Pos[1] 100
execute store result score #z apRigQ run data get entity @s Pos[2] 100
execute store result score #w apRigQ run data get entity @s Rotation[0] 100
execute if score #x apRigQ = @s apRigQx if score #y apRigQ = @s apRigQy if score #z apRigQ = @s apRigQz if score #w apRigQ = @s apRigQw run return 0
scoreboard players operation @s apRigQx = #x apRigQ
scoreboard players operation @s apRigQy = #y apRigQ
scoreboard players operation @s apRigQz = #z apRigQ
scoreboard players operation @s apRigQw = #w apRigQ
execute if score @s apRigFy matches 1.. run return run function rlk:mboss/apep/rig/follow/sink
execute if score @s apRigFl matches 1 run return run function rlk:mboss/apep/rig/follow/burrowed
function rlk:mboss/apep/rig/follow/all
