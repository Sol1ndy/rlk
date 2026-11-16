# Hook intro_tick (@s = body, #mbT 1..; rlk_mb_inv). The intro sequence (150 t clip, seq/intro or the stand-in)
# on the clock #sq kn; music phase 1 at 136 (core); the fight at its end.
execute if score #mbT mb matches 1 run function rlk:boss/arlecchino/core/intro/begin
execute unless score #mbT mb matches 1 run scoreboard players add #sq kn 1
execute unless score #mbT mb matches 1 run function rlk:boss/arlecchino/seq/intro/tick
execute if score #sq kn matches 136 run function rlk:mboss/music/set {ph:1}
execute if score #sqdone kn matches 1 run function rlk:boss/arlecchino/core/intro/done
execute if score #sq kn matches 152.. run function rlk:boss/arlecchino/core/intro/done
function rlk:boss/arlecchino/rig/tick
