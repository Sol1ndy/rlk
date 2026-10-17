# sweep_e clip tick 32
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w6]
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/e1/32
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/e2/32
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/e3/32
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/e4/32
