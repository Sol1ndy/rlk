# Test 36: CS1 now, skipped at its tick 100.
execute unless function rlk:boss/scarlet/core/force run return 0
scoreboard players set #fl hr 0
function rlk:boss/scarlet/core/cs1/start
scoreboard players set #skp hr 100
