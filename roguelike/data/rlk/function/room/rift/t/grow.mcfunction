# Growing (20 t): sparks pour out, the arcs flicker; then open.
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/arcs
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/open
execute if score @s riftT matches 20.. run function rlk:room/rift/open_now
