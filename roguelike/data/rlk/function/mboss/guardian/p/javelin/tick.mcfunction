# P2 tick (@s = body, #gdPT = clip tick). Damage comes from the line; the flying spear is visual only.
execute if score #gdPT mb matches 10 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score #gdPT mb matches 11 run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.8 1.3 0.3
execute if score #gdPT mb matches 11..28 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ^-1.5 ^1.5 ^0.3 0.25 0.25 0.05 0 2 force @a[tag=player]
execute if score #gdPT mb matches 24 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #gdPT mb matches 24 run scoreboard players set #hzSfx mb 3
execute if score #gdPT mb matches 24 run scoreboard players set #hzAct mb 2
execute if score #gdPT mb matches 24 run scoreboard players set #hzKB mb 2
execute if score #gdPT mb matches 24 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:400,w:10,tell:12,dmg:130}
execute if score #gdPT mb matches 28 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.6} ^-1.5 ^1.5 ^0.3 0.05 1.2 0.05 0 20 force @a[tag=player]
execute if score #gdPT mb matches 28 run playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.8 0.3
execute if score #gdPT mb matches 35 run function rlk:mboss/guardian/voice/attack
execute if score #gdPT mb matches 35 run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score #gdPT mb matches 35 run playsound minecraft:entity.firework_rocket.blast hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.3
execute if score #gdPT mb matches 36 run function rlk:mboss/guardian/p/javelin/throw
execute if score #gdPT mb matches 63 run playsound minecraft:item.trident.return hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.3
execute if score #gdPT mb matches 76 run function rlk:mboss/guardian/p/end
