# The decision (@s = body, the end of the recovery): the test hold, the reserved phase step (a floor was reached),
# the test lock, a forced next entry, the rear rule, the far rule, the weighted pick of the band (cooldowns, no
# immediate repeat, MID_MAX).
execute if score #lock hr matches 1 run return run scoreboard players set #rec hr 10
execute if score #fl hr matches 1 if score #ph hr matches 1 run return run function rlk:boss/scarlet/core/cs1/start
execute if score #fl hr matches 2 if score #ph hr matches 7 run return run function rlk:boss/scarlet/core/lead/a13
function rlk:boss/scarlet/ai/sample
execute if score #mbLock mb matches 1 run return run function rlk:boss/scarlet/core/start/a1
execute if score #mbLock mb matches 2 run return run function rlk:boss/scarlet/core/start/a2
execute if score #mbLock mb matches 3 run return run function rlk:boss/scarlet/core/start/a3
execute if score #mbLock mb matches 4 run return run function rlk:boss/scarlet/core/start/a4
execute if score #mbLock mb matches 5 run return run function rlk:boss/scarlet/core/start/a6
execute if score #mbLock mb matches 6 run return run function rlk:boss/scarlet/core/start/a9
execute if score #mbLock mb matches 7 run return run function rlk:boss/scarlet/core/start/a10
execute if score #ai_nx hr matches 3 run return run function rlk:boss/scarlet/ai/next_a3
function rlk:boss/scarlet/ai/rear_count
execute if score #ai_rc hr matches 4.. if function rlk:boss/scarlet/ai/rear run return 1
execute if score #ai_ff hr matches 1 if function rlk:boss/scarlet/ai/after_a6 run return 1
execute if score #far hr matches 30.. run return run function rlk:boss/scarlet/ai/far
execute if score #ph hr matches 1 if score #ai_d2 hr matches ..202500 run return run function rlk:boss/scarlet/ai/pick/p1_near
execute if score #ph hr matches 1 if score #ai_d2 hr matches ..1210000 run return run function rlk:boss/scarlet/ai/pick/p1_mid
execute if score #ph hr matches 1 run return run function rlk:boss/scarlet/ai/pick/p1_far
execute if score #ph hr matches 7 if score #ai_d2 hr matches ..202500 run return run function rlk:boss/scarlet/ai/pick/p2_near
execute if score #ph hr matches 7 if score #ai_d2 hr matches ..1210000 run return run function rlk:boss/scarlet/ai/pick/p2_mid
execute if score #ph hr matches 7 run return run function rlk:boss/scarlet/ai/pick/p2_far
function rlk:boss/scarlet/ai/none
