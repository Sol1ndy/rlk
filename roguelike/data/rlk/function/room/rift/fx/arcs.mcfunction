# @s = the anchor (every 2 t open / growing / entering, every 6 t dormant): the arc frames and their roll.
scoreboard players operation #riftF room = @s riftT
scoreboard players operation #riftF room /= #riftC2 room
scoreboard players operation #riftRl room = #riftF room
scoreboard players operation #riftRl room %= #riftC2 room
scoreboard players operation #riftSt room = @s riftS
execute as @e[tag=rlk_rift_arc,type=minecraft:item_display] if score @s zid = #riftZid room run function rlk:room/rift/fx/arc
