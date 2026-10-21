# Drop the running arena job (cb/remove, uninstall, a 200-t chunk wait): no job, the half-built arena loses its stamp
# and its look record (look_<aid>: a half-swapped look is no look).
execute if data storage rlk:mboss arjob{aid:"az_cavern"} run data remove storage rlk:mboss built_az_cavern
execute if data storage rlk:mboss arjob{aid:"cp_test"} run data remove storage rlk:mboss built_cp_test
execute if data storage rlk:mboss arjob{aid:"az_cavern"} run data remove storage rlk:mboss look_az_cavern
execute if data storage rlk:mboss arjob{aid:"cp_test"} run data remove storage rlk:mboss look_cp_test
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
schedule clear rlk:mboss/arena/job_tick
