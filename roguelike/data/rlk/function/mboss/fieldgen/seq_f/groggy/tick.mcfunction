# S3 groggy (@s = body, #fgT 1..200): slow sparks drip from the slumped core every 40 t (spec Q17), two creaks.
scoreboard players operation #fgM mb = #fgT mb
scoreboard players operation #fgM mb %= #fgK40 mb
execute if score #fgM mb matches 20 positioned ~ ~2.492 ~ run function rlk:mboss/fieldgen/fx/p/groggy_sparks
execute if score #fgM mb matches 20 run function rlk:mboss/fieldgen/fx/snd/groggy_spark
execute if score #fgT mb matches 40 run playsound minecraft:block.anvil.place hostile @a[tag=player] ~ ~ ~ 0.3 0.5 0.1
execute if score #fgT mb matches 120 run playsound minecraft:block.anvil.place hostile @a[tag=player] ~ ~ ~ 0.3 0.5 0.1
