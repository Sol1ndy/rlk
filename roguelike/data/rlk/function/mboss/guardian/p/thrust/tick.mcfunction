# P1 tick (@s = body, #gdPT = clip tick).
execute if score #gdPT mb matches 4..16 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:0.9} ^-0.5 ^2.0 ^1.2 0.3 0.1 0.3 0 2 force @a[tag=player]
execute if score #gdPT mb matches 7 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.9 0.3
execute if score #gdPT mb matches 16 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #gdPT mb matches 16 run scoreboard players set #hzSfx mb 3
execute if score #gdPT mb matches 16 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:55,w:22,tell:12,dmg:100}
execute if score #gdPT mb matches 19 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.4 ^1.9 ^2.6",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.1,s1:0.9,move:"0f,0f,0f",life:6,fade:3}
execute if score #gdPT mb matches 26..28 run function rlk:mboss/mv/step {d:0.9}
execute if score #gdPT mb matches 28 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"burst",pos:"^ ^1.2 ^1.6",rot:"~ ~",bb:"center",roll:0,spin:20,s0:0.6,s1:2.6,move:"0f,0f,0f",life:5,fade:2}
execute if score #gdPT mb matches 28 run playsound minecraft:item.trident.hit hostile @a[tag=player] ~ ~ ~ 1 0.8 0.3
execute if score #gdPT mb matches 28 run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
execute if score #gdPT mb matches 28 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.3
execute if score #gdPT mb matches 38..54 run function rlk:mboss/mv/away {d:0.25}
execute if score #gdPT mb matches 42 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #gdPT mb matches 42 run scoreboard players set #hzSfx mb 3
execute if score #gdPT mb matches 42 run scoreboard players set #hzKB mb 4
execute if score #gdPT mb matches 42 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:70,w:20,tell:16,dmg:115}
execute if score #gdPT mb matches 54 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.3
execute if score #gdPT mb matches 57..58 run function rlk:mboss/mv/step {d:2.8}
execute if score #gdPT mb matches 58 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"burst",pos:"^ ^1.0 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:20,s0:0.6,s1:2.8,move:"0f,0f,0f",life:5,fade:2}
execute if score #gdPT mb matches 58 run playsound minecraft:item.trident.hit hostile @a[tag=player] ~ ~ ~ 1 0.75 0.3
execute if score #gdPT mb matches 58 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.45 1.5 0.3
execute if score #gdPT mb matches 72 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.3
execute if score #gdPT mb matches 91 run function rlk:mboss/guardian/p/end
