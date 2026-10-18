# Hook death_tick (@s = body, #mbT = 1.. until cur.death): the clip runs while the rig ticks; it must NOT tick
# after its kill at 100 (it would respawn).
execute if score #mbT mb matches 1..99 run function rlk:mboss/butterfly/rig_stub/tick
execute if score #mbT mb matches 100 run function rlk:mboss/butterfly/rig_stub/kill
execute if score #bfTcN mb matches 1.. run function rlk:mboss/butterfly/tc/all
execute if score #mbT mb matches 6 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/fx/death_shatter
execute if score #mbT mb matches 24 run playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.27
execute if score #mbT mb matches 24 run playsound minecraft:entity.iron_golem.step hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
execute if score #mbT mb matches 24 run particle minecraft:poof ~ ~0.2 ~ 0.5 0.05 0.5 0.02 8 force @a[tag=player]
execute if score #mbT mb matches 40 run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
execute if score #mbT mb matches 40 run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score #bfM mb matches 0 if score #mbT mb matches 40..96 run function rlk:mboss/butterfly/fx/death_motes
execute if score #mbT mb matches 58 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.8 0.2
execute if score #mbT mb matches 74 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
execute if score #mbT mb matches 88 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
execute if score #mbT mb matches 96 run function rlk:mboss/butterfly/fx/death_end
