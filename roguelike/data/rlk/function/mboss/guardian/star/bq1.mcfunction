# @s = body: queued punishment of break 1 (6 % of max HP as true damage, may be lethal).
scoreboard players remove #gdBq1 mb 1
execute if score #gdBq1 mb matches 1.. run return 0
scoreboard players operation #mbTrueEl mb = #gdBe1 mb
execute rotated 0 0 run function rlk:mboss/guardian/fx/break_ring
function rlk:mboss/true_pct {pct:6}
