# Start the look job "plain" of cp_test (1 slices; the stamp goes until done stamps "cp_test@1:plain";
# look_cp_test = "plain" from now on).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_cp_test
data modify storage rlk:mboss arjob set value {aid:"cp_test",kind:"look",look:"plain",i:0,n:1,wait:0}
scoreboard players set #mbArBuild mb 1
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_cp_test set value "plain"
