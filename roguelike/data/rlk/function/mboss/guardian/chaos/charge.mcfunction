# @s = body, charge clock c = #gdT - #gdCh0: flare 7, red orb 16-30, rise 30, hover 36 -> timer and stars.
scoreboard players operation #gdCc mb = #gdT mb
scoreboard players operation #gdCc mb -= #gdCh0 mb
execute if score #gdCc mb matches 7 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.45f,0.25f],scale:1.4} ^-0.4 ^2.3 ^1.6 0.2 0.2 0.2 0 14 force @a[tag=player]
execute if score #gdCc mb matches 7 run playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.8 1.5 0.3
execute if score #gdCc mb matches 16..30 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.35f,0.32f],scale:1.7} ^ ^2.4 ^0.6 0.25 0.25 0.25 0 3 force @a[tag=player]
execute if score #gdCc mb matches 16..30 run execute rotated as @s rotated ~ 0 run particle minecraft:reverse_portal ^ ^2.4 ^0.6 0.4 0.4 0.4 0.02 2 force @a[tag=player]
execute if score #gdCc mb matches 30 run playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.3
execute if score #gdCc mb matches 36.. run function rlk:mboss/guardian/chaos/hold_start
