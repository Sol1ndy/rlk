# Hook intro_tick (@s = body, #mbT 1..; rlk_mb_inv): the intro (seq/intro or the stand-in, 640 t) on #sq, the skip
# input, the look requests; the fight at its end (#sqdone) or at the framework cap.
execute if score #mbT mb matches 1 run function rlk:boss/scarlet/core/intro/begin
execute unless score #mbT mb matches 1 run scoreboard players add #sq hr 1
execute unless score #mbT mb matches 1 run function rlk:boss/scarlet/core/sq/intro/tick
execute if score #sq_sig hr matches 1.. run scoreboard players set #sq_sig hr 0
function rlk:boss/scarlet/core/skip
execute if score #sqdone hr matches 1 run function rlk:boss/scarlet/core/intro/done
execute if score #sq hr matches 642.. run function rlk:boss/scarlet/core/intro/done
function rlk:boss/scarlet/core/look
function rlk:boss/scarlet/rig_stub/tick
