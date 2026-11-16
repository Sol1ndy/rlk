# @s = the server (arena/job_tick), in minecraft:overworld: one step of the running job of az_cavern.
execute unless function rlk:mboss/ar/az_cavern/loaded run return run function rlk:mboss/arena/az_cavern/wait
data modify storage rlk:mboss arjob.wait set value 0
execute if data storage rlk:mboss arjob{kind:"verify"} run return run function rlk:mboss/arena/az_cavern/vdone
execute store result score #arI mb run data get storage rlk:mboss arjob.i
scoreboard players remove #mbArBuild mb 1
execute store result storage rlk:mboss arjob.i int 1 run scoreboard players add #arI mb 1
scoreboard players remove #arI mb 1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 0 run function rlk:mboss/arena/az_cavern/s/0
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 1 run function rlk:mboss/arena/az_cavern/s/1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 2 run function rlk:mboss/arena/az_cavern/s/2
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 3 run function rlk:mboss/arena/az_cavern/s/3
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 4 run function rlk:mboss/arena/az_cavern/s/4
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 5 run function rlk:mboss/arena/az_cavern/s/5
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 6 run function rlk:mboss/arena/az_cavern/s/6
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 7 run function rlk:mboss/arena/az_cavern/s/7
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 8 run function rlk:mboss/arena/az_cavern/s/8
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 9 run function rlk:mboss/arena/az_cavern/s/9
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 10 run function rlk:mboss/arena/az_cavern/s/10
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 11 run function rlk:mboss/arena/az_cavern/s/11
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 12 run function rlk:mboss/arena/az_cavern/s/12
