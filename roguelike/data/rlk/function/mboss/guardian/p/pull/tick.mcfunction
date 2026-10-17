# P4 tick (@s = body, #gdPT = 0..: pull clip ticks, then swing clip ticks + 44).
execute if score #gdPT mb matches 1..31 run function rlk:mboss/guardian/rig/face/track
execute if score #gdPT mb matches 1..31 run execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.75f,0.1f,0.18f],scale:1.8} ^ ^1.8 ^-0.6 0.6 0.8 0.3 0 2 force @a[tag=player]
execute if score #gdPT mb matches 11..31 run execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.4} ~ ~1 ~ 0.35 0.9 0.35 0 6 force @a[tag=player]
execute if score #gdPT mb matches 11..31 run execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.06f,0f,0f],scale:1.2} ~ ~0.6 ~ 0.3 0.6 0.3 0 3 force @a[tag=player]
execute if score #gdPT mb matches 28 run effect give @a[tag=player] minecraft:darkness 1 0 true
execute if score #gdPT mb matches 32 run execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1.3 positioned ~ 201 ~ run function rlk:mboss/pull/start {t:0}
execute if score #gdPT mb matches 32 run playsound minecraft:entity.enderman.teleport hostile @a[tag=player] ~ ~ ~ 0.9 0.6 0.3
execute if score #gdPT mb matches 32 run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
execute if score #gdPT mb matches 32 run playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
execute if score #gdPT mb matches 44 run function rlk:mboss/guardian/rig/play/swing
execute if score #gdPT mb matches 44 run scoreboard players set #hzSfx mb 2
execute if score #gdPT mb matches 44 run execute at @s positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:55,a:180,tell:20,dmg:120}
execute if score #gdPT mb matches 57 run scoreboard players set #hzSfx mb 2
execute if score #gdPT mb matches 57 run execute at @s positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:55,a:180,tell:20,dmg:120}
execute if score #gdPT mb matches 64 run particle minecraft:sweep_attack ~ ~1.1 ~ 2.6 0.1 2.6 0 10 force @a[tag=player]
execute if score #gdPT mb matches 64 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1.2} ~ ~1.1 ~ 2.8 0.05 2.8 0 30 force @a[tag=player]
execute if score #gdPT mb matches 64 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.3
execute if score #gdPT mb matches 77 run particle minecraft:sweep_attack ~ ~1.4 ~ 2.6 0.3 2.6 0 10 force @a[tag=player]
execute if score #gdPT mb matches 77 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1.3} ~ ~1.4 ~ 2.8 0.3 2.8 0 30 force @a[tag=player]
execute if score #gdPT mb matches 77 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.3
execute if score #gdPT mb matches 95 run function rlk:mboss/guardian/p/end
