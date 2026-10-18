# S3 the break clip (@s = body, #fgT 1..34): the metallic groan of the tilt and wobble (14), a spark and
# a chain creak as it sinks (24).
execute if score #fgT mb matches 14 run function rlk:mboss/fieldgen/fx/snd/groggy_wobble
execute if score #fgT mb matches 24 positioned ~ ~3 ~ run function rlk:mboss/fieldgen/fx/p/spark
execute if score #fgT mb matches 24 run playsound minecraft:block.chain.step hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
