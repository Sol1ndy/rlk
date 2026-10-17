# P3 tick (@s = body, #gdPT = clip tick): disc r 5 centred 3.5 b in front (K25), ring lead 17 t.
execute if score #gdPT mb matches 9 run scoreboard players set #hzSfx mb 4
execute if score #gdPT mb matches 9 run scoreboard players set #hzKB mb 3
execute if score #gdPT mb matches 9 run execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:50,tell:17,dmg:160}
execute if score #gdPT mb matches 12 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.3 ^4.6 ^0.2",rot:"~ ~",bb:"center",roll:0,spin:60,s0:0.1,s1:1.1,move:"0f,0f,0f",life:8,fade:3}
execute if score #gdPT mb matches 12 run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.3
execute if score #gdPT mb matches 26 run execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 run function rlk:fx/nv/card {kind:"burst",pos:"~ 202.2 ~",rot:"~ ~",bb:"center",roll:0,spin:20,s0:0.8,s1:3.4,move:"0f,0f,0f",life:6,fade:3}
execute if score #gdPT mb matches 26 run execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.6} ~ 202.5 ~ 0.15 2 0.15 0 24 force @a[tag=player]
execute if score #gdPT mb matches 26 run execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 run particle minecraft:block{block_state:"minecraft:gold_block"} ~ 201.3 ~ 2 0.2 2 0 30 force @a[tag=player]
execute if score #gdPT mb matches 26 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.3
execute if score #gdPT mb matches 26 run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 0.9 0.3
execute if score #gdPT mb matches 26 run playsound minecraft:item.trident.thunder hostile @a[tag=player] ~ ~ ~ 0.3 1.2 0.3
execute if score #gdPT mb matches 48 run playsound minecraft:block.chain.break hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.3
execute if score #gdPT mb matches 48 run playsound minecraft:block.stone.break hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.3
execute if score #gdPT mb matches 54 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.3
execute if score #gdPT mb matches 70 run function rlk:mboss/guardian/p/end
