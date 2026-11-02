# Tests: make the fight state ready for a forced action (@s = body). Fails during a transition / replay.
execute if score #mbSt mb matches 0 run function rlk:boss/arlecchino/core/intro/done
execute if score #pat kn matches 51.. run return fail
execute if score #pat kn matches 1..49 run function rlk:boss/arlecchino/core/cancel_pat
execute if score #stun kn matches 1 run function rlk:boss/arlecchino/core/stun_end
return 1
