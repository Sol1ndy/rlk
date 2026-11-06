# @s = boss in phase 1/2/3: drop the armor state without the exhausted break. A test keeps the weapon: the forced
# switch that normal_return queues (tag rlk_rd_switch_due) is dropped again.
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/hazard/vfx_world
function rlk:boss/raiden/normal_return
tag @s remove rlk_rd_switch_due
