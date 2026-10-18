# @s = heal orb, at it (1.1 b above the floor).
scoreboard players add #bfDewN mb 1
scoreboard players add @s mbT 1
scoreboard players operation #bfM mb = @s mbT
scoreboard players operation #bfM mb %= #bfK3 mb
execute if score #bfM mb matches 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.9} ~ ~ ~ 0.22 0.22 0.22 0 2 force @a[tag=player]
execute if score #bfM mb matches 1 run particle minecraft:end_rod ~ ~0.2 ~ 0.15 0.25 0.15 0.004 1 force @a[tag=player]
scoreboard players operation #bfM mb = @s mbT
scoreboard players operation #bfM mb %= #bfK10 mb
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0 ~0.12 ~0.8 0 0 0 0 1 force @a[tag=player]
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0.57 ~0.12 ~0.57 0 0 0 0 1 force @a[tag=player]
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0.8 ~0.12 ~0 0 0 0 0 1 force @a[tag=player]
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0.57 ~0.12 ~-0.57 0 0 0 0 1 force @a[tag=player]
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0 ~0.12 ~-0.8 0 0 0 0 1 force @a[tag=player]
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-0.57 ~0.12 ~-0.57 0 0 0 0 1 force @a[tag=player]
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-0.8 ~0.12 ~0 0 0 0 0 1 force @a[tag=player]
execute if score #bfM mb matches 0 positioned ~ ~-1.1 ~ run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-0.57 ~0.12 ~0.57 0 0 0 0 1 force @a[tag=player]
execute positioned ~ ~-1.1 ~ if entity @e[tag=rlk_body,distance=..1.6,limit=1] run function rlk:mboss/butterfly/dew/take
