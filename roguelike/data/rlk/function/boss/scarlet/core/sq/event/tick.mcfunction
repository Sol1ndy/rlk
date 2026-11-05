# Stand-in event tick (#sq hr 1..120).
execute if score #sq hr matches 34 run function rlk:boss/scarlet/rig_stub/play/ev_leave
execute if score #sq hr matches 40 run function rlk:boss/scarlet/rig_stub/state/hidden
execute if score #sq hr matches 56 run function rlk:boss/scarlet/core/sq/event/k/56
execute if score #sq hr matches 120.. run scoreboard players set #sqdone hr 1
