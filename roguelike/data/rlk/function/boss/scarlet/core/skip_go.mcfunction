# The intro skip (@s = body): the prompt gone, the sequence's skip (the black, its state at tick 1290), then the
# clock jumps: the next tick is 1290.
function rlk:boss/scarlet/fx/hud/skip {s:5}
scoreboard players set #skip hr -1
scoreboard players set #skp hr 0
function rlk:boss/scarlet/seq/intro/skip
scoreboard players set #sq hr 1289
