# @s = body: a new cube stream in the first free slot (at most 3), from above her shoulders.
execute store result score #gdR mb run random value 18..30
scoreboard players operation #gdCsT mb = #gdR mb
scoreboard players set #gdCsS mb 0
execute unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs3] run scoreboard players set #gdCsS mb 3
execute unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2] run scoreboard players set #gdCsS mb 2
execute unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1] run scoreboard players set #gdCsS mb 1
execute if score #gdCsS mb matches 0 run return 0
execute if score #gdCsS mb matches 1 run function rlk:mboss/guardian/chaos/cs1/spawn
execute if score #gdCsS mb matches 2 run function rlk:mboss/guardian/chaos/cs2/spawn
execute if score #gdCsS mb matches 3 run function rlk:mboss/guardian/chaos/cs3/spawn
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.25 0.6 0
