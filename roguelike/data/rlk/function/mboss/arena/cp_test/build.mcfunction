# Start a full build job of cp_test (2 slices, one per tick; the stamp goes until done).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_cp_test
data modify storage rlk:mboss arjob set value {aid:"cp_test",kind:"build",look:"plain",i:0,n:2,wait:0}
scoreboard players set #mbArBuild mb 2
schedule function rlk:mboss/arena/job_tick 1t replace
