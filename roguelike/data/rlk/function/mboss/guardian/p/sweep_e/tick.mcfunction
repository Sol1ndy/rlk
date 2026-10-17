# Enchanted sweep tick (@s = body, #gdPT = clip tick).
execute if score #gdPT mb matches 4..6 run execute if score #gdSwEl mb matches 1 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.541f,0.298f],scale:1.2} ^ ^1.7 ^0.3 1.6 0.04 0.04 0 8 force @a[tag=player]
execute if score #gdPT mb matches 7..18 run execute if score #gdSwEl mb matches 1 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.541f,0.298f],scale:1} ^0.8 ^3.2 ^0.2 0.3 0.6 0.3 0 2 force @a[tag=player]
execute if score #gdPT mb matches 4..6 run execute if score #gdSwEl mb matches 2 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.361f,0.784f,1f],scale:1.2} ^ ^1.7 ^0.3 1.6 0.04 0.04 0 8 force @a[tag=player]
execute if score #gdPT mb matches 7..18 run execute if score #gdSwEl mb matches 2 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.361f,0.784f,1f],scale:1} ^0.8 ^3.2 ^0.2 0.3 0.6 0.3 0 2 force @a[tag=player]
execute if score #gdPT mb matches 4..6 run execute if score #gdSwEl mb matches 3 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.894f,0.518f,0.988f],scale:1.2} ^ ^1.7 ^0.3 1.6 0.04 0.04 0 8 force @a[tag=player]
execute if score #gdPT mb matches 7..18 run execute if score #gdSwEl mb matches 3 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.894f,0.518f,0.988f],scale:1} ^0.8 ^3.2 ^0.2 0.3 0.6 0.3 0 2 force @a[tag=player]
execute if score #gdPT mb matches 4..6 run execute if score #gdSwEl mb matches 4 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.635f,0.996f,0.992f],scale:1.2} ^ ^1.7 ^0.3 1.6 0.04 0.04 0 8 force @a[tag=player]
execute if score #gdPT mb matches 7..18 run execute if score #gdSwEl mb matches 4 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.635f,0.996f,0.992f],scale:1} ^0.8 ^3.2 ^0.2 0.3 0.6 0.3 0 2 force @a[tag=player]
execute if score #gdPT mb matches 4 run playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.3
execute if score #gdPT mb matches 5 run playsound minecraft:entity.warden.sonic_charge hostile @a[tag=player] ~ ~ ~ 0.25 1.6 0.3
execute if score #gdPT mb matches 19..27 run function rlk:mboss/guardian/p/sweep_e/strike
execute if score #gdPT mb matches 19 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^ ^1.1 ^",rot:"~ ~",bb:"fixed",roll:0,spin:-150,s0:8,s1:9.8,move:"0f,0f,0f",life:7,fade:2}
execute if score #gdPT mb matches 19 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.3
execute if score #gdPT mb matches 19 run execute if score #gdSwEl mb matches 3 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.5 1.8 0.3
execute if score #gdPT mb matches 19 run execute if score #gdSwEl mb matches 1 run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.3
execute if score #gdPT mb matches 19 run execute if score #gdSwEl mb matches 2 run playsound minecraft:entity.player.splash.high_speed hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
execute if score #gdPT mb matches 19 run execute if score #gdSwEl mb matches 4 run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.8 1.3 0.3
execute if score #gdPT mb matches 50 run function rlk:mboss/guardian/p/end
