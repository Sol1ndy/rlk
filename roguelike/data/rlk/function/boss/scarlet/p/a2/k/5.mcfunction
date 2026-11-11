# A2 pattern tick 5
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_a212] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_a212,limit=1] ^-0.597 ^2.748 ^0.694
