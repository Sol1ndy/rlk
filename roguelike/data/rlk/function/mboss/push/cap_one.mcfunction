# @s = the anchor: the capsule pq[0] (tenths -> mb); the player's anchor-frame position is #mbLf / #mbLs (mb).
execute store result score #pF0 mb run data get storage rlk:mboss pq[0].f0 100
execute store result score #pF1 mb run data get storage rlk:mboss pq[0].f1 100
execute store result score #pHW mb run data get storage rlk:mboss pq[0].hw 100
execute store result score #pTop mb run data get storage rlk:mboss pq[0].top
scoreboard players set #pAct mb 1
data modify storage rlk:mboss pc set from storage rlk:mboss pq[0]
execute unless data storage rlk:mboss pc{px:""} run function rlk:mboss/push/cap_top with storage rlk:mboss pc
execute if score #pAct mb matches 0 run return 0
execute if score #mbLf mb < #pF0 mb run return 0
execute if score #mbLf mb > #pF1 mb run return 0
scoreboard players operation #pAs mb = #mbLs mb
execute if score #pAs mb matches ..-1 run scoreboard players operation #pAs mb *= #cm1 mb
execute if score #pAs mb >= #pHW mb run return 0
# inside: the three exits (distance to the edge, mb) tried nearest first
scoreboard players operation #pdS mb = #pHW mb
scoreboard players operation #pdS mb -= #pAs mb
scoreboard players operation #pdF mb = #pF1 mb
scoreboard players operation #pdF mb -= #mbLf mb
scoreboard players operation #pdB mb = #mbLf mb
scoreboard players operation #pdB mb -= #pF0 mb
scoreboard players set #pU1 mb 0
scoreboard players set #pU2 mb 0
scoreboard players set #pU3 mb 0
scoreboard players set #pEx mb 0
function rlk:mboss/push/pick
execute if score #pEx mb matches 0 run function rlk:mboss/push/pick
execute if score #pEx mb matches 0 run function rlk:mboss/push/pick
execute if score #pEx mb matches 0 run return 0
scoreboard players set #puDone mb 1
function rlk:mboss/push/move
