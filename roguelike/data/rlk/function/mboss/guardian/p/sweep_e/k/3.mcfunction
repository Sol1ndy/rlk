# sweep_e clip tick 3
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/e1/3
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/e2/3
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/e3/3
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/e4/3
