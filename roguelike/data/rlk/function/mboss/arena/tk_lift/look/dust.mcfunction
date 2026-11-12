# Start the look job "dust" of tk_lift (2 slices; the stamp goes until done stamps "tk_lift@1:dust";
# look_tk_lift = "dust" from now on).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_tk_lift
data modify storage rlk:mboss arjob set value {aid:"tk_lift",kind:"look",look:"dust",i:0,n:2,wait:0}
scoreboard players set #mbArBuild mb 2
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_tk_lift set value "dust"
