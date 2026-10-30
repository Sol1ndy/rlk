# Open: arcs every 2 t (frame) / 4 t (roll), particles every 2 t, the rim breathing every 20 t, ambient sound every
# 40 t; the walk-in dwell (10 t within 1 b horizontal and 1.5 b vertical).
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/arcs
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/open
scoreboard players operation #riftQ room = @s riftT
scoreboard players operation #riftQ room %= #riftC40 room
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/ambient
execute if score #riftQ room matches 0 run scoreboard players set #riftB room 0
execute if score #riftQ room matches 20 run scoreboard players set #riftB room 1
execute if score #riftQ room matches 0 run function rlk:room/rift/look/breathe
execute if score #riftQ room matches 20 run function rlk:room/rift/look/breathe
function rlk:room/rift/dwell
