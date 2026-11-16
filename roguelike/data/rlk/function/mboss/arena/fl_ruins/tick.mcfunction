# @s = the server (arena/job_tick), in minecraft:overworld: one step of the running job of fl_ruins.
execute unless function rlk:mboss/ar/fl_ruins/loaded run return run function rlk:mboss/arena/fl_ruins/wait
data modify storage rlk:mboss arjob.wait set value 0
execute if data storage rlk:mboss arjob{kind:"verify"} run return run function rlk:mboss/arena/fl_ruins/vdone
execute store result score #arI mb run data get storage rlk:mboss arjob.i
scoreboard players remove #mbArBuild mb 1
execute store result storage rlk:mboss arjob.i int 1 run scoreboard players add #arI mb 1
scoreboard players remove #arI mb 1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 0 run function rlk:mboss/arena/fl_ruins/s/0
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 1 run function rlk:mboss/arena/fl_ruins/s/1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 2 run function rlk:mboss/arena/fl_ruins/s/2
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 3 run function rlk:mboss/arena/fl_ruins/s/3
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 4 run function rlk:mboss/arena/fl_ruins/s/4
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 5 run function rlk:mboss/arena/fl_ruins/s/5
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 6 run function rlk:mboss/arena/fl_ruins/s/6
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 7 run function rlk:mboss/arena/fl_ruins/s/7
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 8 run function rlk:mboss/arena/fl_ruins/s/8
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 9 run function rlk:mboss/arena/fl_ruins/s/9
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 10 run function rlk:mboss/arena/fl_ruins/s/10
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 11 run function rlk:mboss/arena/fl_ruins/s/11
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 12 run function rlk:mboss/arena/fl_ruins/s/12
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 13 run function rlk:mboss/arena/fl_ruins/s/13
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 14 run function rlk:mboss/arena/fl_ruins/s/14
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 15 run function rlk:mboss/arena/fl_ruins/s/15
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 16 run function rlk:mboss/arena/fl_ruins/s/16
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 17 run function rlk:mboss/arena/fl_ruins/s/17
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 18 run function rlk:mboss/arena/fl_ruins/s/18
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 19 run function rlk:mboss/arena/fl_ruins/s/19
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 20 run function rlk:mboss/arena/fl_ruins/s/20
execute if data storage rlk:mboss arjob{kind:"look",look:"day"} if score #arI mb matches 0 run function rlk:mboss/arena/fl_ruins/l/day/0
execute if data storage rlk:mboss arjob{kind:"look",look:"day"} if score #arI mb matches 1 run function rlk:mboss/arena/fl_ruins/l/day/1
execute if data storage rlk:mboss arjob{kind:"look",look:"day"} if score #arI mb matches 2 run function rlk:mboss/arena/fl_ruins/l/day/2
execute if data storage rlk:mboss arjob{kind:"look",look:"day"} if score #arI mb matches 3 run function rlk:mboss/arena/fl_ruins/l/day/3
execute if data storage rlk:mboss arjob{kind:"look",look:"crimson"} if score #arI mb matches 0 run function rlk:mboss/arena/fl_ruins/l/crimson/0
execute if data storage rlk:mboss arjob{kind:"look",look:"crimson"} if score #arI mb matches 1 run function rlk:mboss/arena/fl_ruins/l/crimson/1
execute if data storage rlk:mboss arjob{kind:"look",look:"crimson"} if score #arI mb matches 2 run function rlk:mboss/arena/fl_ruins/l/crimson/2
execute if data storage rlk:mboss arjob{kind:"look",look:"crimson"} if score #arI mb matches 3 run function rlk:mboss/arena/fl_ruins/l/crimson/3
