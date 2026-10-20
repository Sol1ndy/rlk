# A player at the centre: the bearing toward the arena arrival spot (cur.start) instead. Only the bearing counts
# (ring_land divides by the length), so the offset is taken in units of 4 mb: up to 128 b on x / z without overflow.
execute store result score #qx mb run data get storage rlk:mboss cur.start.x 1000
execute store result score #qz mb run data get storage rlk:mboss cur.start.z 1000
scoreboard players operation #qx mb -= #qcx mb
scoreboard players operation #qz mb -= #qcz mb
scoreboard players set #t mb 4
scoreboard players operation #qx mb /= #t mb
scoreboard players operation #qz mb /= #t mb
execute unless score #qx mb matches -32000..32000 run return 0
execute unless score #qz mb matches -32000..32000 run return 0
scoreboard players operation #n mb = #qx mb
scoreboard players operation #n mb *= #qx mb
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= #qz mb
scoreboard players operation #n mb += #t mb
execute if score #n mb matches ..0 run return 0
function rlk:mboss/push/sqrt
function rlk:mboss/push/ring_land
