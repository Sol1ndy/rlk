# A13 pattern tick 75.
function rlk:boss/scarlet/g/st/side
function rlk:boss/scarlet/rig/play/g_dash
function rlk:boss/scarlet/g/spot/d1
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
execute at @s run function rlk:boss/scarlet/fx/snd/g_appear
function rlk:boss/scarlet/g/cut/make {s:89,t:14,dmg:37,kb:0,n:1}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_67]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_69] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_71] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
