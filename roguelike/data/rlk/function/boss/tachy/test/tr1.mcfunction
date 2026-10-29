# Test 22: T1 날개 전개 now (then P2).
execute unless function rlk:boss/tachy/core/force run return 0
scoreboard players set #fl tk 1
scoreboard players set #ph tk 2
scoreboard players operation #mbFloor mb = #fl35 tk
function rlk:boss/tachy/core/tr/start
