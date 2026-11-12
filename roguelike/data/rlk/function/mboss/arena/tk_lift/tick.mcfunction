# @s = the server (arena/job_tick), in minecraft:overworld: one step of the running job of tk_lift.
execute unless function rlk:mboss/ar/tk_lift/loaded run return run function rlk:mboss/arena/tk_lift/wait
data modify storage rlk:mboss arjob.wait set value 0
execute if data storage rlk:mboss arjob{kind:"verify"} run return run function rlk:mboss/arena/tk_lift/vdone
execute store result score #arI mb run data get storage rlk:mboss arjob.i
scoreboard players remove #mbArBuild mb 1
execute store result storage rlk:mboss arjob.i int 1 run scoreboard players add #arI mb 1
scoreboard players remove #arI mb 1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 0 run function rlk:mboss/arena/tk_lift/s/0
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 1 run function rlk:mboss/arena/tk_lift/s/1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 2 run function rlk:mboss/arena/tk_lift/s/2
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 3 run function rlk:mboss/arena/tk_lift/s/3
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 4 run function rlk:mboss/arena/tk_lift/s/4
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 5 run function rlk:mboss/arena/tk_lift/s/5
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 6 run function rlk:mboss/arena/tk_lift/s/6
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 7 run function rlk:mboss/arena/tk_lift/s/7
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 8 run function rlk:mboss/arena/tk_lift/s/8
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 9 run function rlk:mboss/arena/tk_lift/s/9
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 10 run function rlk:mboss/arena/tk_lift/s/10
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 11 run function rlk:mboss/arena/tk_lift/s/11
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 12 run function rlk:mboss/arena/tk_lift/s/12
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 13 run function rlk:mboss/arena/tk_lift/s/13
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 14 run function rlk:mboss/arena/tk_lift/s/14
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 15 run function rlk:mboss/arena/tk_lift/s/15
execute if data storage rlk:mboss arjob{kind:"look",look:"dust"} if score #arI mb matches 0 run function rlk:mboss/arena/tk_lift/l/dust/0
execute if data storage rlk:mboss arjob{kind:"look",look:"dust"} if score #arI mb matches 1 run function rlk:mboss/arena/tk_lift/l/dust/1
execute if data storage rlk:mboss arjob{kind:"look",look:"abyss"} if score #arI mb matches 0 run function rlk:mboss/arena/tk_lift/l/abyss/0
execute if data storage rlk:mboss arjob{kind:"look",look:"abyss"} if score #arI mb matches 1 run function rlk:mboss/arena/tk_lift/l/abyss/1
