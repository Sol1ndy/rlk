# The intro skip (@s = the body): the prompt gone, the sequence's skip (the black, its state at tick 1290), then the
# clock jumps: the next tick is 1290. #sq_skn: the rest of this tick's timeline is not played.
function rlk:boss/scarlet/seq/intro/skipoff
scoreboard players set #skp hr 0
function rlk:boss/scarlet/seq/intro/skip
scoreboard players set #sq hr 1289
scoreboard players set #sq_skn hr 1
