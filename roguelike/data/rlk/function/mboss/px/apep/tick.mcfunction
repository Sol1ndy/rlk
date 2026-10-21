# @s = the body of apep (the anchor), at it, after the module and rig ticks: the key of the shown clip tick (the anchor's
# apRigT; negative = queued: the offsets stay), then every proxy follows the anchor.
execute unless score @s apRigT matches 0.. run return run function rlk:mboss/px/apep/follow with storage rlk:mboss px.o
execute store result score #pxC mb run scoreboard players get @s apRigC
scoreboard players operation #pxT mb = @s apRigT
function rlk:mboss/px/apep/c
function rlk:mboss/px/apep/follow with storage rlk:mboss px.o
