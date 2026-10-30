# Dormant (the room's fight runs): one slow arc, a third of the open particles (every 6 t), not enterable.
scoreboard players operation #riftQ room = @s riftT
scoreboard players set #riftK room 6
scoreboard players operation #riftQ room %= #riftK room
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/arcs
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/dust
