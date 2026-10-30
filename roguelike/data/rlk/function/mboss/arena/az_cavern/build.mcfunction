# Start a full build job of az_cavern (13 slices, one per tick; the stamp goes until done; look_az_cavern = "default").
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_az_cavern
data modify storage rlk:mboss arjob set value {aid:"az_cavern",kind:"build",look:"default",i:0,n:13,wait:0}
scoreboard players set #mbArBuild mb 13
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_az_cavern set value "default"
