# sweep_e clip tick 24
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w3]
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/e1/24
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/e2/24
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/e3/24
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/e4/24
