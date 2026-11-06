# The stamp of cp_test is right but the box is not loaded: a 1-slice job that waits for the chunks, then checks
# the sentinel (done -> stamp kept; wrong -> a full build).
execute if score #mbArBuild mb matches 1.. run return fail
data modify storage rlk:mboss arjob set value {aid:"cp_test",kind:"verify",look:"plain",i:0,n:1,wait:0}
scoreboard players set #mbArBuild mb 1
schedule function rlk:mboss/arena/job_tick 1t replace
