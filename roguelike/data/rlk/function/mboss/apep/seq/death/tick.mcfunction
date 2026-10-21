# STUB (AP-CORE, ap_contract 1.6): the pattern stage AP-P1 replaces this file.
# @s = body, #apPT = 0..: the seed shows at the sink (t100).
execute if score #apPT mb matches 100 run data merge entity @e[type=minecraft:item_display,tag=rlk_mb_ap_seed,limit=1] {start_interpolation:0,interpolation_duration:10,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f]}}
