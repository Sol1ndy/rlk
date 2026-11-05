# The gauntlet set #done (@s = body; S4: at REPEL_T after a deflect, at FAIL60_P2_T after the A8 fail): #gres decides.
# A8: deflect -> CS2 (repel {at:60}); fail -> P2 (the fail-60 hit and g_reform were the gauntlet's). A13: deflect -> CS3
# (repel {at:5}); fail (the instant death did not end the run) -> the revive stance -> A13 again.
scoreboard players set #done hr 0
scoreboard players set #pat hr 0
scoreboard players set #pt hr 0
execute if score #gres hr matches 1 run return run function rlk:boss/scarlet/core/repel/start
execute if score #gk hr matches 1 run return run function rlk:boss/scarlet/core/p2/from_fail
function rlk:boss/scarlet/core/revive/start
