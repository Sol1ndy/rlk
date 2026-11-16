# Internal: the root and the parts to the execution position and yaw; the avatar hidden.
execute rotated ~ 0 run tp @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_cine_part] ~ ~ ~ ~ 0
function rlk:char/cine/hide
