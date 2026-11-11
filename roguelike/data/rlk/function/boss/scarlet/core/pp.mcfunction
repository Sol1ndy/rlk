# hr_design §1.5: a perfect parry on the running pattern's last / single hit (@s = body; the pattern's PP window): she
# flinches (clip flinch) and the pattern ends 6 t later (core/ppf instead of its tick).
execute if score #ppf hr matches 1.. run return 0
scoreboard players set #ppf hr 6
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/rig/play/flinch
kill @e[type=minecraft:item_display,tag=rlk_hr_trb]
tag @e[type=minecraft:item_display,tag=rlk_hr_trg] remove rlk_hr_trg
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute as @e[type=minecraft:item_display,tag=rlk_hr_trf] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_trq] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tri] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_2"
