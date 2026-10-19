# @s = the body of cproto (the anchor), at it, after the module and rig ticks: the key of the shown clip tick (the anchor's
# mbT; negative = queued: the offsets stay), then every proxy follows the anchor.
execute unless score @s mbT matches 0.. run return run function rlk:mboss/px/cproto/follow with storage rlk:mboss px.o
execute store result score #pxC mb run scoreboard players get @s mbS
scoreboard players operation #pxT mb = @s mbT
function rlk:mboss/px/cproto/c
function rlk:mboss/px/cproto/follow with storage rlk:mboss px.o
