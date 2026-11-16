# Test 20: E70 now (from P1a: the floor counts as reached; later: the event again).
execute unless function rlk:boss/arlecchino/core/force run return 0
scoreboard players set #e70 kn 0
function rlk:boss/arlecchino/core/e70_go
