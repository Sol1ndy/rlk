# Start a full build job of tk_lift (16 slices, one per tick; the stamp goes until done; look_tk_lift = "dust").
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_tk_lift
data modify storage rlk:mboss arjob set value {aid:"tk_lift",kind:"build",look:"dust",i:0,n:16,wait:0}
scoreboard players set #mbArBuild mb 16
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_tk_lift set value "dust"
