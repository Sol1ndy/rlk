# Start a full build job of hr_field (21 slices, one per tick; the stamp goes until done; look_hr_field = "moon").
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_hr_field
data modify storage rlk:mboss arjob set value {aid:"hr_field",kind:"build",look:"moon",i:0,n:21,wait:0}
scoreboard players set #mbArBuild mb 21
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_hr_field set value "moon"
