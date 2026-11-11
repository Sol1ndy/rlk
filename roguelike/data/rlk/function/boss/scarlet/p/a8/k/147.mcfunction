# A8 pattern tick 147.
kill @e[type=minecraft:marker,tag=rlk_hr_gst]
function rlk:boss/scarlet/g/spot/side
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] add rlk_hr_gst
tag @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] remove rlk_hr_gsp
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c139_141]
function rlk:boss/scarlet/rig/play/g_drop
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_flash
execute at @s run function rlk:boss/scarlet/fx/snd/g_flash
function rlk:boss/scarlet/g/cut/make {s:163,t:16,dmg:37,kb:0,n:1}
