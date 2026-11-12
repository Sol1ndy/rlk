# Tests: make the fight state ready for a forced action (@s = body). Fails during a mantle / transition / replay.
execute if score #mbSt mb matches 0 run function rlk:boss/tachy/core/intro/done
execute if score #pat tk matches 51.. run return fail
execute if score #pat tk matches 1..11 run function rlk:boss/tachy/core/cancel_pat
execute if score #pat tk matches 50 run scoreboard players set #pat tk 0
execute if score #stag tk matches 1.. run function rlk:boss/tachy/core/stag_end
return 1
