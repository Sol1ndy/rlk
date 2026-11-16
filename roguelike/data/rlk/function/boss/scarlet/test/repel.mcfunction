# Test 24: the repel {at:60} now (then P2).
execute unless function rlk:boss/scarlet/core/force run return 0
function rlk:boss/scarlet/test/prep
scoreboard players set #gk hr 1
function rlk:boss/scarlet/core/repel/start
