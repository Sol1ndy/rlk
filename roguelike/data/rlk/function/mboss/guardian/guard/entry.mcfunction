# @s = body, guard clock 1..50: baton twirl, vertical spin discs (16-35), gold ground ring (35), settle.
# Discs and ring are telegraphs only (no damage, K24).
function rlk:mboss/guardian/rig/face/track
execute if score #gdT mb matches 6 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.6 0.9 0.3
execute if score #gdT mb matches 11 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.3
execute if score #gdT mb matches 16 run function rlk:fx/nv/card {kind:"ring",pos:"^-1.3 ^1.6 ^0.2",rot:"~90 0",bb:"fixed",roll:0,spin:140,s0:0.5,s1:3.4,move:"0f,0f,0f",life:10,fade:4}
execute if score #gdT mb matches 22 run function rlk:fx/nv/card {kind:"ring",pos:"^ ^1.6 ^1.4",rot:"~ 0",bb:"fixed",roll:0,spin:140,s0:0.5,s1:3.4,move:"0f,0f,0f",life:10,fade:4}
execute if score #gdT mb matches 28 run function rlk:fx/nv/card {kind:"ring",pos:"^1.1 ^1.6 ^1.0",rot:"~-45 0",bb:"fixed",roll:0,spin:140,s0:0.5,s1:3.4,move:"0f,0f,0f",life:10,fade:4}
execute if score #gdT mb matches 16 run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 0.6 1 0.3
execute if score #gdT mb matches 16 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.9 1.6 0.3
execute if score #gdT mb matches 22 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.9 1.8 0.3
execute if score #gdT mb matches 28 run playsound minecraft:entity.illusioner.cast_spell hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.3
execute if score #gdT mb matches 28..35 run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.2 ~ 1.2 0.1 1.2 0 3 force @a[tag=player]
execute if score #gdT mb matches 35 run function rlk:fx/nv/card {kind:"ring",pos:"~ ~0.1 ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1,s1:9.4,move:"0f,0f,0f",life:9,fade:4}
execute if score #gdT mb matches 35 run playsound minecraft:block.amethyst_block.place hostile @a[tag=player] ~ ~ ~ 1 0.5 0.3
execute if score #gdT mb matches 35 run playsound minecraft:entity.iron_golem.step hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.3
execute if score #gdT mb matches 36..44 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~0.15 ~ 2.4 0.02 2.4 0 6 force @a[tag=player]
execute if score #gdT mb matches 50.. run function rlk:mboss/guardian/guard/open
