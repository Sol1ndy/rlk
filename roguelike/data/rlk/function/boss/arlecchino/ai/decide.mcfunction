# The decision (@s = body, end of the recovery). Order: test hold, the reserved phase step (a floor was reached:
# E70 / T), the test lock (#mbLock), Q0 (P2 opener), the schedules (F / Q5), the rear rule (P2: Q3), the far rule,
# the weighted pick of the phase column / band (cooldowns, no immediate repeat, A within reach, Q6 first use).
execute if score #lock kn matches 1 run return run scoreboard players set #rec kn 10
execute if score #fl kn matches 1 run return run function rlk:boss/arlecchino/core/e70_go
execute if score #fl kn matches 2 run return run function rlk:boss/arlecchino/core/tr/start
function rlk:boss/arlecchino/ai/sample
execute if score #mbLock mb matches 1 run return run function rlk:boss/arlecchino/core/start/a2
execute if score #mbLock mb matches 2 run return run function rlk:boss/arlecchino/core/start/a5
execute if score #mbLock mb matches 3 run return run function rlk:boss/arlecchino/core/start/b1
execute if score #mbLock mb matches 4 run return run function rlk:boss/arlecchino/core/start/b2
execute if score #mbLock mb matches 5 run return run function rlk:boss/arlecchino/core/start/c1
execute if score #mbLock mb matches 6 run return run function rlk:boss/arlecchino/core/start/c2
execute if score #mbLock mb matches 7 run return run function rlk:boss/arlecchino/core/start/d1
execute if score #mbLock mb matches 8 run return run function rlk:boss/arlecchino/core/start/d2
execute if score #mbLock mb matches 9 run return run function rlk:boss/arlecchino/core/start/e1
execute if score #mbLock mb matches 10 run return run function rlk:boss/arlecchino/core/start/f1
execute if score #mbLock mb matches 11 run return run function rlk:boss/arlecchino/core/start/g1
execute if score #mbLock mb matches 12 run return run function rlk:boss/arlecchino/core/start/h1
execute if score #mbLock mb matches 13 run return run function rlk:boss/arlecchino/core/start/a4
execute if score #ph kn matches 3 if score #clk kn >= #sch_f kn if score #ai_nf kn matches 3.. run return run function rlk:boss/arlecchino/ai/go_f_p1b
execute if score #far kn matches 40.. if function rlk:boss/arlecchino/ai/far run return 1
execute if score #ph kn matches 1 if score #ai_d2 kn matches ..202500 run return run function rlk:boss/arlecchino/ai/pick/p1a_near
execute if score #ph kn matches 1 if score #ai_d2 kn matches ..1210000 run return run function rlk:boss/arlecchino/ai/pick/p1a_mid
execute if score #ph kn matches 1 run return run function rlk:boss/arlecchino/ai/pick/p1a_far
execute if score #ph kn matches 3 if score #ai_d2 kn matches ..202500 run return run function rlk:boss/arlecchino/ai/pick/p1b_near
execute if score #ph kn matches 3 if score #ai_d2 kn matches ..1210000 run return run function rlk:boss/arlecchino/ai/pick/p1b_mid
execute if score #ph kn matches 3 run return run function rlk:boss/arlecchino/ai/pick/p1b_far
function rlk:boss/arlecchino/ai/none
