# The skip (@s = body): the prompt gone, the sequence's skip (the black, the intro cleared, her E10 pose ≤ 7 b
# from the player), then the clock jumps: the next tick is 554 (intro_end 0, line 11).
function rlk:boss/scarlet/fx/hud/skip {s:5}
scoreboard players set #skip hr -1
scoreboard players set #skp hr 0
function rlk:boss/scarlet/seq/intro/skip
scoreboard players set #sq hr 553
