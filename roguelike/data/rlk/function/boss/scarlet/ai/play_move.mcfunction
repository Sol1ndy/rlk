# The recovery clip (@s = body): walk / P2 glide in, strafe left / right (P2 the idle2 stance between).
execute if score #ai_mv hr matches 1 run return run function rlk:boss/scarlet/rig_stub/play/walk
execute if score #ai_mv hr matches 5 run return run function rlk:boss/scarlet/rig_stub/play/glide
execute if score #ai_mv hr matches 2 run return run function rlk:boss/scarlet/rig_stub/play/strafe_l
execute if score #ai_mv hr matches 3 run return run function rlk:boss/scarlet/rig_stub/play/strafe_r
execute if score #ph hr matches 7 run return run function rlk:boss/scarlet/rig_stub/play/idle2
function rlk:boss/scarlet/rig_stub/play/idle
