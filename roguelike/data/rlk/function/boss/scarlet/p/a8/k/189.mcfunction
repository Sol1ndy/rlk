# A8 pattern tick 189.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_183]
function rlk:boss/scarlet/g/cut/lock {s:196}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^-0.617 ^2.048 ^0.661 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:3}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c196] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c196,limit=1] ^-0.979 ^2.501 ^0.986
