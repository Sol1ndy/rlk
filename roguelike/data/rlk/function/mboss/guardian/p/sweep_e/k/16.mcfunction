# sweep_e clip tick 16
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/s0_1
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/s0_2
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/s0_3
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/s0_4
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
