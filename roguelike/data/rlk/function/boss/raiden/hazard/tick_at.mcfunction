# Advance this hazard at its fixed origin and frozen yaw.
scoreboard players add @s rdHAge 1
execute if score @s rdHAge >= @s rdHLife run return run function rlk:boss/raiden/hazard/expire
scoreboard players operation #rdUntil rd = @s rdWind
scoreboard players operation #rdUntil rd -= @s rdHAge
execute if score #rdUntil rd matches 1..4 run function rlk:boss/raiden/hazard/charge
scoreboard players operation #rdMod rd = @s rdHAge
scoreboard players set #rdFour rd 4
scoreboard players operation #rdMod rd %= #rdFour rd
execute if score @s rdHAge matches 1.. if score @s rdHAge < @s rdWind if score #rdMod rd matches 0 rotated as @s run function rlk:boss/raiden/hazard/warning
execute unless score @s rdShape matches 11 if score @s rdHAge = @s rdWind rotated as @s run function rlk:boss/raiden/hazard/strike
execute if score @s rdShape matches 11 if score @s rdHAge >= @s rdWind rotated as @s run function rlk:boss/raiden/hazard/ring_tick
