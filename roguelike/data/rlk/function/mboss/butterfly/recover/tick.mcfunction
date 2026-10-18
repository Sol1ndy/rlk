scoreboard players add #bfT mb 1
execute if score #bfT mb matches 1..24 run function rlk:mboss/mv/turn {max:9}
execute if score #bfT mb matches 24 run function rlk:mboss/butterfly/rig_stub/play/chain_reform
execute if score #bfT mb matches 30 run playsound minecraft:block.chain.place hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
execute if score #bfT mb matches 30 run playsound minecraft:block.amethyst_block.place hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
execute if score #bfT mb matches 30 run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.1} ~ ~1.8 ~ 0.6 0.6 0.6 0 10 force @a[tag=player]
execute if score #bfT mb matches 42.. run function rlk:mboss/butterfly/groggy/end
