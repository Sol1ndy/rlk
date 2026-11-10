# The cs1 skip (@s = body): the prompt gone, the sequence's skip (the black, its state at tick 566), then the
# clock jumps: the next tick is 566.
function rlk:boss/scarlet/fx/hud/skip {s:5}
scoreboard players set #skip hr -1
scoreboard players set #skp hr 0
function rlk:boss/scarlet/core/sq/cs1/skip
scoreboard players set #sq hr 565
