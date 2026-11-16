# cs1: the timeline at #sq 614 (@s = the body).
data modify storage rlk:mboss camtx.line set value {text:"",background:0}
function rlk:mboss/cam/text
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.881 ^2.735 ^1.15 run tp @s ~ ~ ~
