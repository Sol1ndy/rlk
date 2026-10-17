# Gold sweep tick (@s = body, #gdPT = clip tick).
execute if score #gdPT mb matches 19 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^ ^1.0 ^",rot:"~ ~",bb:"fixed",roll:0,spin:-150,s0:8,s1:9.6,move:"0f,0f,0f",life:6,fade:2}
execute if score #gdPT mb matches 19 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.3
execute if score #gdPT mb matches 19 run playsound minecraft:block.pointed_dripstone.land hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.3
execute if score #gdPT mb matches 19 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.3 1.3 0.3
execute if score #gdPT mb matches 19..22 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1.3} ^ ^0.6 ^3.2 2.6 0.3 1.4 0 12 force @a[tag=player]
execute if score #gdPT mb matches 44 run function rlk:mboss/guardian/p/end
