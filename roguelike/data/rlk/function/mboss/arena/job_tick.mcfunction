# The one running arena job (rlk:mboss arjob, #mbArBuild = slices left): one step per tick, re-scheduled while
# it runs (mboss/init re-arms it after /reload).
execute unless score #mbArBuild mb matches 1.. run return run data remove storage rlk:mboss arjob
execute if data storage rlk:mboss arjob{aid:"az_cavern"} in minecraft:overworld run function rlk:mboss/arena/az_cavern/tick
execute if data storage rlk:mboss arjob{aid:"ap_oasis"} in minecraft:overworld run function rlk:mboss/arena/ap_oasis/tick
execute if data storage rlk:mboss arjob{aid:"cp_test"} in minecraft:overworld run function rlk:mboss/arena/cp_test/tick
execute unless data storage rlk:mboss arjob run scoreboard players set #mbArBuild mb 0
execute if score #mbArBuild mb matches 1.. run schedule function rlk:mboss/arena/job_tick 1t replace
