# @s = the zone marker: 1 when the 3 x 3 footprint (#riftPx / #riftPz +- 1) stays off every pit warning box, else fail.
data modify storage rlk:room rpq set value []
data modify storage rlk:room rpq set from entity @s data.pits
scoreboard players operation #riftA0 room = #riftPx room
scoreboard players add #riftA0 room 1
scoreboard players operation #riftA1 room = #riftPx room
scoreboard players remove #riftA1 room 1
scoreboard players operation #riftA2 room = #riftPz room
scoreboard players add #riftA2 room 1
scoreboard players operation #riftA3 room = #riftPz room
scoreboard players remove #riftA3 room 1
return run function rlk:room/rift/spot/pit_loop
