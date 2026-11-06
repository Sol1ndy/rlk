# Crimson haze (K21): dust columns at the arena rim and ash over the arena, every 4 t.
scoreboard players operation #gdM mb = #gdT mb
scoreboard players operation #gdM mb %= #gdK4 mb
execute unless score #gdM mb matches 0 run return 0
scoreboard players operation #gdM mb = #gdT mb
scoreboard players operation #gdM mb /= #gdK4 mb
scoreboard players operation #gdM mb %= #gdK4 mb
execute if score #gdM mb matches 0 run function rlk:mboss/guardian/chaos/haze0
execute if score #gdM mb matches 1 run function rlk:mboss/guardian/chaos/haze1
execute if score #gdM mb matches 2 run function rlk:mboss/guardian/chaos/haze2
execute if score #gdM mb matches 3 run function rlk:mboss/guardian/chaos/haze3
particle minecraft:dust{color:[0.59f,0.2f,0.27f],scale:2.2} 200 208 8 12 4 12 0 6 force @a[tag=player]
