# Start a full build job of fl_ruins (21 slices, one per tick; the stamp goes until done; look_fl_ruins = "day").
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_fl_ruins
data modify storage rlk:mboss arjob set value {aid:"fl_ruins",kind:"build",look:"day",i:0,n:21,wait:0}
scoreboard players set #mbArBuild mb 21
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_fl_ruins set value "day"
