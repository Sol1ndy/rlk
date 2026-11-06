# Change a live hazard's size (@s = its marker), tenths of a block: {r, r0} = outer / inner radius of a disc, ring,
# sector or full (r0 = the safe hole) or the length / back of a line, {w} = the width of a line (0 = keep). The
# hit bounds are recomputed with the 0.3 b body pad (as hz/init). Meant for #hzQuiet hazards whose visual the module
# draws (the framework outline of a loud one is redrawn too). Score form without a macro: set #hzSzR #hzSzR0
# #hzSzW mb and call hz/resize_s (an expanding wave front calls it every tick).
$scoreboard players set #hzSzR mb $(r)
$scoreboard players set #hzSzR0 mb $(r0)
$scoreboard players set #hzSzW mb $(w)
function rlk:mboss/hz/resize_s
