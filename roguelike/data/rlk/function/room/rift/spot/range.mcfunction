# The cell rlk:room sc: x / z ranges of block centres >= 3 b inside its wall faces (a side whose sx equals ix is an
# open join to the next cell: its whole spawn range counts). #riftRg room 0 when the cell is too small.
scoreboard players set #riftRg room 0
execute store result score #riftS0 room run data get storage rlk:room sc.sx0
execute store result score #riftS1 room run data get storage rlk:room sc.sx1
execute store result score #riftI0 room run data get storage rlk:room sc.ix0
execute store result score #riftI1 room run data get storage rlk:room sc.ix1
scoreboard players operation #riftLo room = #riftS0 room
execute if score #riftS0 room > #riftI0 room run scoreboard players operation #riftLo room = #riftI0 room
execute if score #riftS0 room > #riftI0 room run scoreboard players add #riftLo room 3
scoreboard players operation #riftHi room = #riftS1 room
execute if score #riftS1 room < #riftI1 room run scoreboard players operation #riftHi room = #riftI1 room
execute if score #riftS1 room < #riftI1 room run scoreboard players remove #riftHi room 3
execute if score #riftLo room > #riftHi room run return 0
execute store result storage rlk:room rsr.x0 int 1 run scoreboard players get #riftLo room
execute store result storage rlk:room rsr.x1 int 1 run scoreboard players get #riftHi room
execute store result score #riftS0 room run data get storage rlk:room sc.sz0
execute store result score #riftS1 room run data get storage rlk:room sc.sz1
execute store result score #riftI0 room run data get storage rlk:room sc.iz0
execute store result score #riftI1 room run data get storage rlk:room sc.iz1
scoreboard players operation #riftLo room = #riftS0 room
execute if score #riftS0 room > #riftI0 room run scoreboard players operation #riftLo room = #riftI0 room
execute if score #riftS0 room > #riftI0 room run scoreboard players add #riftLo room 3
scoreboard players operation #riftHi room = #riftS1 room
execute if score #riftS1 room < #riftI1 room run scoreboard players operation #riftHi room = #riftI1 room
execute if score #riftS1 room < #riftI1 room run scoreboard players remove #riftHi room 3
execute if score #riftLo room > #riftHi room run return 0
execute store result storage rlk:room rsr.z0 int 1 run scoreboard players get #riftLo room
execute store result storage rlk:room rsr.z1 int 1 run scoreboard players get #riftHi room
function rlk:room/rift/spot/rand with storage rlk:room rsr
data modify storage rlk:room rsp.y set from entity @s data.cy
scoreboard players set #riftRg room 1
