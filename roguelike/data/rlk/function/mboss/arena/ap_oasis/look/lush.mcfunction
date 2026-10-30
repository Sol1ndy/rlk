# Start the look job "lush" of ap_oasis (23 slices; the stamp goes until done stamps "ap_oasis@1:lush";
# look_ap_oasis = "lush" from now on).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_ap_oasis
data modify storage rlk:mboss arjob set value {aid:"ap_oasis",kind:"look",look:"lush",i:0,n:23,wait:0}
scoreboard players set #mbArBuild mb 23
schedule function rlk:mboss/arena/job_tick 1t replace
data modify storage rlk:mboss look_ap_oasis set value "lush"
