# G1 swap (@s = body): 24 t standing; she drags the blade through her palm, the edge changes at tick 14.
scoreboard players set #pat tk 50
scoreboard players set #pt tk 0
scoreboard players set #done tk 0
execute if score #el tk matches 1 run function rlk:boss/tachy/rig_stub/play/swap_electro
execute if score #el tk matches 3 run function rlk:boss/tachy/rig_stub/play/swap_pyro
execute if score #el tk matches 1 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
execute if score #el tk matches 1 run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
execute if score #el tk matches 3 run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
execute if score #el tk matches 3 run playsound minecraft:block.fire.extinguish hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
function rlk:boss/tachy/hud/sub
