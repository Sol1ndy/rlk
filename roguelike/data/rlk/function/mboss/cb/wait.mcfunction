# @s = zone marker: the arena is not ready yet (being built or restored, its chunks loading, or another arena's job
# running). Retry in 10 t; 7 misses in a row while no job runs (#mbArBuild 0) or 60 retries in all cancel (the gate
# returns with the same cprep).
scoreboard players add #cbWait mb 1
execute if score #cbWait mb matches 60.. run return run function rlk:mboss/start_cancel
execute if score #mbArBuild mb matches 1.. run return run scoreboard players set #spawnT room 10
scoreboard players add #mbLd mb 1
execute if score #mbLd mb matches ..6 run return run scoreboard players set #spawnT room 10
function rlk:mboss/start_cancel
