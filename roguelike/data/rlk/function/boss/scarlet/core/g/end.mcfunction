# The gauntlet set #done (@s = body; at the judge with the gauge at 0, at FAIL60_P2_T after the G1 fail, 12 t after a
# survived G2 fail): #gres decides. Gauge 0 -> the repel {at:60} (G1) / {at:5} (G2), started in this tick. G1 fail -> P2
# (the fail-60 hit and g_reform were the gauntlet's). G2 fail (the instant death did not end the run) -> the revive
# stance -> G2 again. A test's forced fail (#pipoff, tests 23 / 29) applies to this one judge only.
scoreboard players set #done hr 0
scoreboard players set #pat hr 0
scoreboard players set #pt hr 0
scoreboard players set #pipoff hr 0
execute if score #gres hr matches 1 run return run function rlk:boss/scarlet/core/repel/start
execute if score #gk hr matches 1 run return run function rlk:boss/scarlet/core/p2/from_fail
function rlk:boss/scarlet/core/revive/start
