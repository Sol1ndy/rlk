# A player at the centre: the bearing toward the arena arrival spot (cur.start) instead.
execute store result score #qx mb run data get storage rlk:mboss cur.start.x 1000
execute store result score #qz mb run data get storage rlk:mboss cur.start.z 1000
scoreboard players operation #qx mb -= #qcx mb
scoreboard players operation #qz mb -= #qcz mb
execute unless score #qx mb matches -40000..40000 run return 0
execute unless score #qz mb matches -40000..40000 run return 0
scoreboard players operation #n mb = #qx mb
scoreboard players operation #n mb *= #qx mb
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= #qz mb
scoreboard players operation #n mb += #t mb
execute if score #n mb matches ..0 run return 0
function rlk:mboss/push/sqrt
function rlk:mboss/push/ring_land
