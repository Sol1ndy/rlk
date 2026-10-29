# The decision (@s = body, end of the recovery). Order: test freeze, the reserved phase step (a floor was reached:
# the mantle), the forced G1 swap, the test lock (#mbLock), the rear rule, the far rule, the weighted pick of the
# phase / band (cooldowns, no immediate repeat, K rules).
execute if score #lock tk matches 1 run return run scoreboard players set #rec tk 10
execute if score #flnext tk matches 1.. run return run function rlk:boss/tachy/mantle/start
execute if score #swt tk >= #ai_swl tk run return run function rlk:boss/tachy/el/swap_start
function rlk:boss/tachy/ai/sample
execute if score #mbLock mb matches 1 run return run function rlk:boss/tachy/core/start/a1
execute if score #mbLock mb matches 2 run return run function rlk:boss/tachy/core/start/b1
execute if score #mbLock mb matches 3 run return run function rlk:boss/tachy/core/start/b2
execute if score #mbLock mb matches 4 run return run function rlk:boss/tachy/core/start/b3
execute if score #mbLock mb matches 5 run return run function rlk:boss/tachy/core/start/c1
execute if score #mbLock mb matches 6 run return run function rlk:boss/tachy/core/start/c2
execute if score #mbLock mb matches 7 run return run function rlk:boss/tachy/core/start/c3
execute if score #mbLock mb matches 8 run return run function rlk:boss/tachy/core/start/k
execute if score #mbLock mb matches 9 run return run function rlk:boss/tachy/core/start/w1
execute if score #mbLock mb matches 10 run return run function rlk:boss/tachy/core/start/w2
execute if score #mbLock mb matches 11 run return run function rlk:boss/tachy/core/start/l
function rlk:boss/tachy/ai/rear_count
execute if score #ai_rc tk matches 4.. if function rlk:boss/tachy/ai/rear run return 1
execute if score #far tk matches 40.. if function rlk:boss/tachy/ai/far run return 1
execute if score #ai_fp tk matches 1 if score #ai_d2 tk matches ..250000 run return run function rlk:boss/tachy/ai/pick/p1_near
execute if score #ai_fp tk matches 1 if score #ai_d2 tk matches ..1440000 run return run function rlk:boss/tachy/ai/pick/p1_mid
execute if score #ai_fp tk matches 1 run return run function rlk:boss/tachy/ai/pick/p1_far
execute if score #ai_fp tk matches 2 if score #ai_d2 tk matches ..250000 run return run function rlk:boss/tachy/ai/pick/p2_near
execute if score #ai_fp tk matches 2 if score #ai_d2 tk matches ..1440000 run return run function rlk:boss/tachy/ai/pick/p2_mid
execute if score #ai_fp tk matches 2 run return run function rlk:boss/tachy/ai/pick/p2_far
execute if score #ai_fp tk matches 3 if score #ai_d2 tk matches ..250000 run return run function rlk:boss/tachy/ai/pick/p3_near
execute if score #ai_fp tk matches 3 if score #ai_d2 tk matches ..1440000 run return run function rlk:boss/tachy/ai/pick/p3_mid
execute if score #ai_fp tk matches 3 run return run function rlk:boss/tachy/ai/pick/p3_far
