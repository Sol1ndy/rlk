# A13 pattern tick 56.
kill @e[type=minecraft:marker,tag=rlk_hr_gst]
function rlk:boss/scarlet/g/spot/over
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s positioned ~ ~2.5 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] add rlk_hr_gst
tag @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] remove rlk_hr_gsp
function rlk:boss/scarlet/g/cut/aim {s:66}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_48]
