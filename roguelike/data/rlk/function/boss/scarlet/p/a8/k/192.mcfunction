# A8 pattern tick 192.
function rlk:boss/scarlet/rig/look/blade/pink
function rlk:boss/scarlet/rig/anchor/blade_tip
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/g_glow
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c196] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c196,limit=1] ^-0.464 ^1.996 ^1.773
