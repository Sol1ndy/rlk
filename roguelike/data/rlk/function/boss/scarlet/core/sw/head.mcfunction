# {d} The target line's head to d blocks along the line (blade.py: d = the line's length x the share of the way it
# shall have run one tick from now).
$execute at @e[type=minecraft:item_display,tag=rlk_hr_swl,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swlh] ^ ^ ^$(d)
