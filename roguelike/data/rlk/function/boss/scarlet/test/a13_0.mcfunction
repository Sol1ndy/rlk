# Test 28: A13 now, with the gauge at 0 (the deflect).
execute unless function rlk:boss/scarlet/core/force run return 0
function rlk:boss/scarlet/test/prep
function rlk:boss/scarlet/shield/arm
scoreboard players set #gau hr 0
scoreboard players set #pipoff hr 0
scoreboard players set #gk hr 2
function rlk:boss/scarlet/core/g/start/a13
