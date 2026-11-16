# Damage number at @s (same look as combat/apply).
function rlk:element/color
execute store result storage rlk:combat dmg int 1 run scoreboard players get #dmg tmp
execute store result storage rlk:combat ox float 0.1 run random value -8..8
execute store result storage rlk:combat oz float 0.1 run random value -8..8
execute store result storage rlk:combat oy float 0.1 run random value 16..26
execute if score #crit tmp matches 1 run function rlk:combat/text_crit_macro with storage rlk:combat
execute unless score #crit tmp matches 1 run function rlk:combat/text_normal_macro with storage rlk:combat
particle minecraft:crit ~ ~1 ~ 0.25 0.35 0.25 0.12 8
