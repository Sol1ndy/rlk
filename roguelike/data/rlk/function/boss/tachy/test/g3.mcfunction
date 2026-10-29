# Test 25: A1 with a reaction inside its core window (the backfire next tick).
execute unless function rlk:boss/tachy/core/force run return 0
function rlk:boss/tachy/core/start/a1
scoreboard players set #core tk 2
