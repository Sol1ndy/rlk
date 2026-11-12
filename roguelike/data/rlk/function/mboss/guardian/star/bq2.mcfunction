# @s = body: queued punishment of break 2 (18 % of max HP as true damage, may be lethal).
scoreboard players remove #gdBq2 mb 1
execute if score #gdBq2 mb matches 1.. run return 0
scoreboard players operation #mbTrueEl mb = #gdBe2 mb
execute rotated 0 0 run function rlk:mboss/guardian/fx/break_ring
function rlk:mboss/true_pct {pct:18}
