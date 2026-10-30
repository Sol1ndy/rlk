# Collapsing (30 t): sparks pulled in, the implosion at the end (close_end).
execute if score #riftQ room matches 0 run particle minecraft:reverse_portal ~ ~1.45 ~ 0.7 1.0 0.7 0.3 8
execute if score #riftQ room matches 0 run particle minecraft:electric_spark ~ ~1.45 ~ 0.3 0.5 0.3 0.05 3
execute if score @s riftT matches 30.. run function rlk:room/rift/close_end
