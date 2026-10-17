# sweep_e clip tick 4
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.3
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/e1/4
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/e2/4
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/e3/4
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/e4/4
