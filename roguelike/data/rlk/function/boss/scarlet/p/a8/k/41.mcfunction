# A8 pattern tick 41.
function rlk:boss/scarlet/g/cut/lock {s:48}
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:3}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c48] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c48,limit=1] ^-1.018 ^0.115 ^0.294
