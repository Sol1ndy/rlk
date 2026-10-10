# Stationary siege unit; command knockback is excluded by shared hit handling.
# Clear an old stagger on reload without touching the separate elemental freeze state.
execute if score @s stunT matches 0.. run function rlk:mob/unstun
data merge entity @s {NoAI:1b,Motion:[0d,0d,0d]}
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
scoreboard players set #hold tmp 1
