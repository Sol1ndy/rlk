# STUB (AP-CORE): the step sounds of the moves (plan 8.1 M); #apMvK 1 crawl, 2 walk, 3-4 steps.
scoreboard players operation #apM mb = #apMvT mb
scoreboard players operation #apM mb %= #apK8 mb
execute if score #apM mb matches 0 run execute if score #apMvK mb matches 1 run playsound minecraft:entity.camel.step hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
scoreboard players operation #apM mb = #apMvT mb
scoreboard players operation #apM mb %= #apK8 mb
execute if score #apM mb matches 0 run execute if score #apMvK mb matches 2 run playsound minecraft:entity.warden.step hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.23
scoreboard players operation #apM mb = #apMvT mb
scoreboard players operation #apM mb %= #apK5 mb
execute if score #apM mb matches 0 run execute if score #apMvK mb matches 3.. run playsound minecraft:block.moss_carpet.step hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.27
