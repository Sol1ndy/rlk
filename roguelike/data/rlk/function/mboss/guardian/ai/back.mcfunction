# @s = body, hop clock #gdT 1..12: she keeps facing the player while gliding back; trail and landing puff.
scoreboard players add #gdT mb 1
function rlk:mboss/guardian/rig/face/track
execute if score #gdT mb matches 1..9 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:0.8} ~ ~0.6 ~ 0.3 0.3 0.3 0 2 force @a[tag=player]
execute if score #gdT mb matches 2..6 run particle minecraft:cloud ~ ~0.2 ~ 0.2 0.05 0.2 0.01 1 force @a[tag=player]
execute if score #gdT mb matches 11 run particle minecraft:poof ~ ~0.15 ~ 0.6 0.05 0.6 0.03 10 force @a[tag=player]
execute if score #gdT mb matches 11 run particle minecraft:block{block_state:"minecraft:calcite"} ~ ~0.1 ~ 0.6 0.05 0.6 0 14 force @a[tag=player]
execute if score #gdT mb matches 11 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~0.12 ~ 0.9 0.02 0.9 0 10 force @a[tag=player]
execute if score #gdT mb matches 11 run playsound minecraft:block.amethyst_block.fall hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
execute if score #gdT mb matches 11 run playsound minecraft:block.calcite.step hostile @a[tag=player] ~ ~ ~ 0.7 0.9 0.23
execute if score #gdT mb matches 12.. run function rlk:mboss/guardian/ai/back_go
