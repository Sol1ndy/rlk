# Air over the box of cp_test when it is loaded (room/remove -> cb/remove), and no stamp (no look record).
execute if data storage rlk:mboss arjob{aid:"cp_test"} run function rlk:mboss/arena/abort
data remove storage rlk:mboss built_cp_test
data remove storage rlk:mboss look_cp_test
execute unless function rlk:mboss/ar/cp_test/loaded run return fail
fill 524 196 -8 556 206 24 minecraft:air strict
fill 524 207 -8 556 216 24 minecraft:air strict
return 1
