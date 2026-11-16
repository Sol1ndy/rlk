# @s = the server (arena/job_tick), in minecraft:overworld: one step of the running job of cp_test.
execute unless function rlk:mboss/ar/cp_test/loaded run return run function rlk:mboss/arena/cp_test/wait
data modify storage rlk:mboss arjob.wait set value 0
execute if data storage rlk:mboss arjob{kind:"verify"} run return run function rlk:mboss/arena/cp_test/vdone
execute store result score #arI mb run data get storage rlk:mboss arjob.i
scoreboard players remove #mbArBuild mb 1
execute store result storage rlk:mboss arjob.i int 1 run scoreboard players add #arI mb 1
scoreboard players remove #arI mb 1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 0 run function rlk:mboss/arena/cp_test/s/0
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 1 run function rlk:mboss/arena/cp_test/s/1
execute if data storage rlk:mboss arjob{kind:"look",look:"plain"} if score #arI mb matches 0 run function rlk:mboss/arena/cp_test/l/plain/0
execute if data storage rlk:mboss arjob{kind:"look",look:"lit"} if score #arI mb matches 0 run function rlk:mboss/arena/cp_test/l/lit/0
