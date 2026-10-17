# P5 tick (@s = body, #gdPT = clip tick). Ring locked at take-off + 2 (K26), 20 t to the impact, r 4.5.
execute if score #gdPT mb matches 0..12 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.25f,0.16f,0.1f],scale:1.2} ^-0.4 ^2.6 ^0.4 0.1 0.6 0.1 0 2 force @a[tag=player]
execute if score #gdPT mb matches 6 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.4 ^4.6 ^0.3",rot:"~ ~",bb:"center",roll:0,spin:60,s0:0.1,s1:1,move:"0f,0f,0f",life:6,fade:3}
execute if score #gdPT mb matches 16 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.6} ~ ~3 ~ 0.15 3 0.15 0 30 force @a[tag=player]
execute if score #gdPT mb matches 16 run playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.3
execute if score #gdPT mb matches 19 run function rlk:mboss/guardian/voice/attack
execute if score #gdPT mb matches 19 run scoreboard players set #mbNoLeash mb 1
execute if score #gdPT mb matches 19 run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.8 1.3 0.3
execute if score #gdPT mb matches 19 run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.7 1 0.3
execute if score #gdPT mb matches 21 run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p5"]}
execute if score #gdPT mb matches 21 run scoreboard players set #hzSfx mb 1
execute if score #gdPT mb matches 21 run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5,limit=1] run function rlk:mboss/hz/disc {r:45,tell:20,dmg:180}
execute if score #gdPT mb matches 21 run tag @s add rlk_mb_inv
execute if score #gdPT mb matches 23 run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5,limit=1] run function rlk:mboss/mv/glide {t:16}
execute if score #gdPT mb matches 26..39 run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5,limit=1] run particle minecraft:end_rod ~ ~6 ~ 0.6 2 0.6 0 1 force @a[tag=player]
execute if score #gdPT mb matches 37 run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.7 1.8 0.3
execute if score #gdPT mb matches 41 run tag @s remove rlk_mb_inv
execute if score #gdPT mb matches 41 run scoreboard players set #mbNoLeash mb 0
execute if score #gdPT mb matches 41 run function rlk:fx/nv/card {kind:"burst",pos:"~ ~1.2 ~",rot:"~ ~",bb:"center",roll:0,spin:20,s0:0.8,s1:3.6,move:"0f,0f,0f",life:6,fade:3}
execute if score #gdPT mb matches 41 run function rlk:fx/nv/card {kind:"ring",pos:"~ ~0.1 ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1,s1:9,move:"0f,0f,0f",life:8,fade:3}
execute if score #gdPT mb matches 41 run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.3 ~ 2.2 0.2 2.2 0 34 force @a[tag=player]
execute if score #gdPT mb matches 41 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 0.9 0.3
execute if score #gdPT mb matches 41 run playsound minecraft:entity.zombie.attack_iron_door hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.3
execute if score #gdPT mb matches 41 run kill @e[type=minecraft:marker,tag=rlk_mb_gd_p5]
execute if score #gdPT mb matches 47 run playsound minecraft:block.pointed_dripstone.land hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
execute if score #gdPT mb matches 47 run playsound minecraft:block.amethyst_cluster.place hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
execute if score #gdPT mb matches 71 run playsound minecraft:block.chain.break hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.3
execute if score #gdPT mb matches 79 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.3
execute if score #gdPT mb matches 101 run function rlk:mboss/guardian/p/end
