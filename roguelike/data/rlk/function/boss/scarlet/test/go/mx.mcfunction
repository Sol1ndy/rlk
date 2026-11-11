# Test 16: MX now.
execute unless function rlk:boss/scarlet/core/force run return 0
execute unless score #ph hr matches 7 run function rlk:boss/scarlet/test/p2
function rlk:boss/scarlet/core/start/mx
