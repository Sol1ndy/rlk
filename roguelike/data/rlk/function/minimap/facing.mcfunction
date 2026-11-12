# #mmDir 0..7: where the player looks, in 45 degree steps (0 south, 2 west, 4 north, 6 east).
execute store result score #mmDir mm run data get entity @a[tag=player,limit=1] Rotation[0] 10
scoreboard players add #mmDir mm 36225
scoreboard players set #c3600 mm 3600
scoreboard players operation #mmDir mm %= #c3600 mm
scoreboard players set #c450 mm 450
scoreboard players operation #mmDir mm /= #c450 mm
