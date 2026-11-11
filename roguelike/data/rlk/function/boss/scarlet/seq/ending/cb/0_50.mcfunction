# ending: the camera, the ticks 0..50.
execute if score #sq hr matches 0 run return run function rlk:boss/scarlet/seq/ending/c/0
execute if score #sq hr matches 46 run return run function rlk:boss/scarlet/seq/ending/c/46
execute if score #sq hr matches 47..49 run return run function rlk:boss/scarlet/seq/ending/c/47_49
execute if score #sq hr matches 50 run return run function rlk:boss/scarlet/seq/ending/c/50
