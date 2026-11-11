# A13 pattern tick 198.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c190_192]
function rlk:boss/scarlet/g/cut/aim {s:206}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c206,limit=1] ^-1.057 ^1.413 ^1.33
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~-130 0 positioned ^ ^ ^5.2 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
