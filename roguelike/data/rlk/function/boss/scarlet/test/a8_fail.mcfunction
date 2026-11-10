# Test 23: A8 now, that fails (no segment can go).
execute unless function rlk:boss/scarlet/core/force run return 0
function rlk:boss/scarlet/test/prep
function rlk:boss/scarlet/shield/arm
scoreboard players set #pipoff hr 1
scoreboard players set #gk hr 1
function rlk:boss/scarlet/core/g/start/a8
