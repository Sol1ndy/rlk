# Drop the running arena job (cb/remove, uninstall, a 200-t chunk wait): no job, the half-built arena loses its stamp.
execute if data storage rlk:mboss arjob{aid:"cp_test"} run data remove storage rlk:mboss built_cp_test
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
schedule clear rlk:mboss/arena/job_tick
