# Start the look job "crimson" of fl_ruins (4 slices; the stamp goes until done stamps "fl_ruins@1:crimson";
# look_fl_ruins = "crimson" from now on).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_fl_ruins
data modify storage rlk:mboss arjob set value {aid:"fl_ruins",kind:"look",look:"crimson",i:0,n:4,wait:0}
scoreboard players set #mbArBuild mb 4
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_fl_ruins set value "crimson"
