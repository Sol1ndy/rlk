# Hook tick (@s = body, at it, fight state #mbSt 1): the phase machine, then the rig tick (the shown clip tick ==
# the pattern / sequence clock).
execute if score #ph hr matches 0 run function rlk:boss/scarlet/core/intro/done
function rlk:boss/scarlet/core/fight
function rlk:boss/scarlet/rig/tick
execute at 524c4b4d-4852-4400-8000-000000000000 run tp @e[type=minecraft:item_display,tag=rlk_hr_trr] ~ ~ ~ ~ ~
