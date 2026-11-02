# T tick (#pat 51): the sequence on #sq; at 140 the P2 pool (repool 36) and music phase 2.
scoreboard players add #sq kn 1
function rlk:boss/arlecchino/seq/t_p2/tick
execute if score #sq kn matches 140 run function rlk:boss/arlecchino/core/tr/title
execute if score #sqdone kn matches 1 run return run function rlk:boss/arlecchino/core/tr/end
execute if score #sq kn matches 220.. run function rlk:boss/arlecchino/core/tr/end
