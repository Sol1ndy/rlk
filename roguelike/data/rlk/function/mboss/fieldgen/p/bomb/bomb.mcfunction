# @s = a falling bomb, at it: down to the floor in 5 t (client-interpolated), burst on its decal.
scoreboard players add @s mbT 1
execute if score @s mbT matches 1 run tp @s ~ ~-4.2 ~
execute if score @s mbT matches 6.. run particle minecraft:explosion ~ ~0.2 ~ 0.2 0.05 0.2 0 1 force @a[tag=player]
execute if score @s mbT matches 6.. run particle minecraft:dust{color:[0.902f,0.698f,0.353f],scale:1.4} ~ ~0.2 ~ 0.5 0.1 0.5 0 6 force @a[tag=player]
execute if score @s mbT matches 6.. run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.45 1.6 0.15
execute if score @s mbT matches 6.. run kill @s
