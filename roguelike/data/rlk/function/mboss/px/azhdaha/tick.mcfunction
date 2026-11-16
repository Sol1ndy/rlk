# @s = the body of azhdaha (the anchor), at it, after the module and rig ticks: the key of the shown clip tick (the anchor's
# azRigT; negative = queued: the offsets stay), then every proxy follows the anchor.
execute unless score @s azRigT matches 0.. run return run function rlk:mboss/px/azhdaha/follow with storage rlk:mboss px.o
execute store result score #pxC mb run scoreboard players get @s azRigC
scoreboard players operation #pxT mb = @s azRigT
function rlk:mboss/px/azhdaha/c
function rlk:mboss/px/azhdaha/follow with storage rlk:mboss px.o
