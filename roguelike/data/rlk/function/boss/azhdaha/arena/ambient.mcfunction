# Ambient particles of the arena element (plan 2.6): gold motes (Geo), drips (Hydro), embers (Pyro), snow
# (Cryo), sparks (Electro), at a random player-near spot.
execute if score #azArEl mb matches 5 at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.95,0.75,0.25],scale:1.2} ~ ~6 ~ 8 3 8 0 4 force @a[tag=player]
execute if score #azArEl mb matches 2 at @e[tag=rlk_body,limit=1] run particle minecraft:dripping_water ~ ~6 ~ 8 3 8 0 4 force @a[tag=player]
execute if score #azArEl mb matches 1 at @e[tag=rlk_body,limit=1] run particle minecraft:lava ~ ~6 ~ 8 3 8 0 4 force @a[tag=player]
execute if score #azArEl mb matches 4 at @e[tag=rlk_body,limit=1] run particle minecraft:snowflake ~ ~6 ~ 8 3 8 0 4 force @a[tag=player]
execute if score #azArEl mb matches 3 at @e[tag=rlk_body,limit=1] run particle minecraft:electric_spark ~ ~6 ~ 8 3 8 0 4 force @a[tag=player]
execute if score #azPh mb matches 3 at @e[tag=rlk_body,limit=1] if score #azLeg mb matches 2 run particle minecraft:dripping_water ~ ~6 ~ 8 3 8 0 2 force @a[tag=player]
execute if score #azPh mb matches 3 at @e[tag=rlk_body,limit=1] if score #azLeg mb matches 1 run particle minecraft:lava ~ ~6 ~ 8 3 8 0 1 force @a[tag=player]
