# B3 pattern tick 30
function rlk:boss/tachy/rig_stub/look/chest/off
execute if score #b3_dl tk matches 0..8 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #b3_dl tk matches 0..8 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #b3_dl tk matches 9..16 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #b3_dl tk matches 9..16 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #b3_dl tk matches 17..24 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #b3_dl tk matches 17..24 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
