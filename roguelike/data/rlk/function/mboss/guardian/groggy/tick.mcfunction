scoreboard players add #gdT mb 1
execute if score #gdT mb matches 8 run function rlk:mboss/guardian/voice/groggy
execute if score #gdT mb matches 18 run playsound minecraft:block.amethyst_block.fall hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
execute if score #gdT mb matches 18 run playsound minecraft:entity.player.attack.knockback hostile @a[tag=player] ~ ~ ~ 0.4 0.8 0.3
scoreboard players operation #gdM mb = #gdT mb
scoreboard players operation #gdM mb %= #gdK6 mb
execute if score #gdM mb matches 0 if score #gdT mb matches 20..136 run function rlk:mboss/guardian/fx/pool
execute if score #gdT mb matches 24 run playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.3
execute if score #gdT mb matches 84 run playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.3
execute if score #gdT mb matches 136 run function rlk:mboss/guardian/rig/play/groggy_b
execute if score #gdT mb matches 170 run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.3
execute if score #gdT mb matches 173 run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.3
execute if score #gdT mb matches 170 run playsound minecraft:item.armor.equip_elytra hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
execute if score #gdT mb matches 220.. run function rlk:mboss/guardian/groggy/end
