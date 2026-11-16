# Start the look job "dark" of hr_field (10 slices; the stamp goes until done stamps "hr_field@1:dark";
# look_hr_field = "dark" from now on).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_hr_field
data modify storage rlk:mboss arjob set value {aid:"hr_field",kind:"look",look:"dark",i:0,n:10,wait:0}
scoreboard players set #mbArBuild mb 10
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_hr_field set value "dark"
