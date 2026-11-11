# A13 pattern tick 160.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c152_154]
function rlk:boss/scarlet/g/cut/aim {s:169}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c169] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c169,limit=1] ^-1.473 ^1.595 ^0.947
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~75 0 positioned ^ ^ ^4.4 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
