# A down-window tick (@s = body): the kipup, the floor wait (lead_down at 0) or the timer.
execute if score #kip hr matches 1.. run return run function rlk:boss/scarlet/core/kip/tick
execute if score #flw hr matches 1.. run scoreboard players remove #flw hr 1
execute if score #fl hr matches 2 if score #flw hr matches ..0 run return run function rlk:boss/scarlet/core/lead/down
execute if score #fl hr matches 2 run return 0
scoreboard players remove #down hr 1
execute if score #down hr matches ..0 run function rlk:boss/scarlet/core/kip/start
