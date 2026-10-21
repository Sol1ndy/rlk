# TEMPORARY (plan §C.3, removed in S3): the release encounter drives the rig through rdAnim / rdPhase. @s = the boss.
# rig_hide (release encounter) moves the parts away: refresh the follow cache while it is in force.
execute if score @s rdHidden matches 1.. run scoreboard players reset @s rdRigQx
execute if score @s rdAnim = @s rdRigL if score @s rdPhase = @s rdRigP run return 0
function rlk:boss/raiden/rig/legacy/changed
