# Entering (the fight starts; the rift stays lit until the fight ends): the flare settles at 6 t, blindness at 20 t.
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/arcs
execute if score #riftQ room matches 0 run function rlk:room/rift/fx/open
execute if score @s riftT matches 6 run function rlk:room/rift/look/open
execute if score @s riftT matches 20 run effect give @a[tag=player] minecraft:blindness 2 0 true
execute if score @s riftT matches ..20 at @e[tag=rlk_body,limit=1] run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.6 0.4 0.6 6
