# cs1: the timeline at #sq 654 (@s = the body).
data modify storage rlk:mboss camtx.line set value {text:"",background:0}
function rlk:mboss/cam/text
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_a,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1.35 ^0.689 ^0.94 run tp @s ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_b,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.846 ^0.402 ^1.234 run tp @s ~ ~ ~
