# fail clip tick 80
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q13r1_6]
execute if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/p/fail/j1/dissolve
