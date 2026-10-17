# sweep_e clip tick 15
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/e1/15
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/e2/15
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/e3/15
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/e4/15
