# Start the look job "crimson" of hr_field (4 slices; the stamp goes until done stamps "hr_field@1:crimson";
# look_hr_field = "crimson" from now on).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_hr_field
data modify storage rlk:mboss arjob set value {aid:"hr_field",kind:"look",look:"crimson",i:0,n:4,wait:0}
scoreboard players set #mbArBuild mb 4
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_hr_field set value "crimson"
