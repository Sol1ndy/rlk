# Stand-in event tick (#sq hr 1..120).
execute if score #sq hr matches 4 run function rlk:boss/scarlet/core/sq/event/k/4
execute if score #sq hr matches 34 run function rlk:boss/scarlet/rig/play/ev_leave
execute if score #sq hr matches 40 run function rlk:boss/scarlet/rig/state/hidden
execute if score #sq hr matches 56 run function rlk:boss/scarlet/core/sq/event/k/56
execute if score #sq hr matches 110 run function rlk:boss/scarlet/fx/hud/ovl {g:"black",in:10,hold:12,out:0}
execute if score #sq hr matches 120.. run scoreboard players set #sqdone hr 1
