# event: the camera, the ticks 0..3.
execute if score #sq hr matches 0 run return run function rlk:boss/scarlet/seq/event/c/0
execute if score #sq hr matches 1..3 run return run function rlk:boss/scarlet/seq/event/c/1_3
