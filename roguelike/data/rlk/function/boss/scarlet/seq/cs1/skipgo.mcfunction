# The cs1 skip (@s = the body): the prompt gone, the sequence's skip (the black, its state at tick 566), then the
# clock jumps: the next tick is 566. #sq_skn: the rest of this tick's timeline is not played.
function rlk:boss/scarlet/seq/cs1/skipoff
scoreboard players set #skp hr 0
function rlk:boss/scarlet/seq/cs1/skip
scoreboard players set #sq hr 565
scoreboard players set #sq_skn hr 1
