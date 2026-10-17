# fail clip tick 68
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q13r0_1]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q13r0_8]
execute if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/p/fail/j1/tint
