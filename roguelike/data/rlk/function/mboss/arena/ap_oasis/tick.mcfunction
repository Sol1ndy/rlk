# @s = the server (arena/job_tick), in minecraft:overworld: one step of the running job of ap_oasis.
execute unless function rlk:mboss/ar/ap_oasis/loaded run return run function rlk:mboss/arena/ap_oasis/wait
data modify storage rlk:mboss arjob.wait set value 0
execute if data storage rlk:mboss arjob{kind:"verify"} run return run function rlk:mboss/arena/ap_oasis/vdone
execute store result score #arI mb run data get storage rlk:mboss arjob.i
scoreboard players remove #mbArBuild mb 1
execute store result storage rlk:mboss arjob.i int 1 run scoreboard players add #arI mb 1
scoreboard players remove #arI mb 1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 0 run function rlk:mboss/arena/ap_oasis/s/0
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 1 run function rlk:mboss/arena/ap_oasis/s/1
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 2 run function rlk:mboss/arena/ap_oasis/s/2
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 3 run function rlk:mboss/arena/ap_oasis/s/3
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 4 run function rlk:mboss/arena/ap_oasis/s/4
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 5 run function rlk:mboss/arena/ap_oasis/s/5
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 6 run function rlk:mboss/arena/ap_oasis/s/6
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 7 run function rlk:mboss/arena/ap_oasis/s/7
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 8 run function rlk:mboss/arena/ap_oasis/s/8
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 9 run function rlk:mboss/arena/ap_oasis/s/9
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 10 run function rlk:mboss/arena/ap_oasis/s/10
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 11 run function rlk:mboss/arena/ap_oasis/s/11
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 12 run function rlk:mboss/arena/ap_oasis/s/12
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 13 run function rlk:mboss/arena/ap_oasis/s/13
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 14 run function rlk:mboss/arena/ap_oasis/s/14
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 15 run function rlk:mboss/arena/ap_oasis/s/15
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 16 run function rlk:mboss/arena/ap_oasis/s/16
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 17 run function rlk:mboss/arena/ap_oasis/s/17
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 18 run function rlk:mboss/arena/ap_oasis/s/18
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 19 run function rlk:mboss/arena/ap_oasis/s/19
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 20 run function rlk:mboss/arena/ap_oasis/s/20
execute if data storage rlk:mboss arjob{kind:"build"} if score #arI mb matches 21 run function rlk:mboss/arena/ap_oasis/s/21
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 0 run function rlk:mboss/arena/ap_oasis/l/withered/0
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 1 run function rlk:mboss/arena/ap_oasis/l/withered/1
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 2 run function rlk:mboss/arena/ap_oasis/l/withered/2
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 3 run function rlk:mboss/arena/ap_oasis/l/withered/3
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 4 run function rlk:mboss/arena/ap_oasis/l/withered/4
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 5 run function rlk:mboss/arena/ap_oasis/l/withered/5
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 6 run function rlk:mboss/arena/ap_oasis/l/withered/6
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 7 run function rlk:mboss/arena/ap_oasis/l/withered/7
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 8 run function rlk:mboss/arena/ap_oasis/l/withered/8
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 9 run function rlk:mboss/arena/ap_oasis/l/withered/9
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 10 run function rlk:mboss/arena/ap_oasis/l/withered/10
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 11 run function rlk:mboss/arena/ap_oasis/l/withered/11
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 12 run function rlk:mboss/arena/ap_oasis/l/withered/12
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 13 run function rlk:mboss/arena/ap_oasis/l/withered/13
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 14 run function rlk:mboss/arena/ap_oasis/l/withered/14
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 15 run function rlk:mboss/arena/ap_oasis/l/withered/15
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 16 run function rlk:mboss/arena/ap_oasis/l/withered/16
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 17 run function rlk:mboss/arena/ap_oasis/l/withered/17
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 18 run function rlk:mboss/arena/ap_oasis/l/withered/18
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 19 run function rlk:mboss/arena/ap_oasis/l/withered/19
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 20 run function rlk:mboss/arena/ap_oasis/l/withered/20
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 21 run function rlk:mboss/arena/ap_oasis/l/withered/21
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 22 run function rlk:mboss/arena/ap_oasis/l/withered/22
execute if data storage rlk:mboss arjob{kind:"look",look:"withered"} if score #arI mb matches 23 run function rlk:mboss/arena/ap_oasis/l/withered/23
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 0 run function rlk:mboss/arena/ap_oasis/l/lush/0
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 1 run function rlk:mboss/arena/ap_oasis/l/lush/1
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 2 run function rlk:mboss/arena/ap_oasis/l/lush/2
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 3 run function rlk:mboss/arena/ap_oasis/l/lush/3
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 4 run function rlk:mboss/arena/ap_oasis/l/lush/4
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 5 run function rlk:mboss/arena/ap_oasis/l/lush/5
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 6 run function rlk:mboss/arena/ap_oasis/l/lush/6
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 7 run function rlk:mboss/arena/ap_oasis/l/lush/7
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 8 run function rlk:mboss/arena/ap_oasis/l/lush/8
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 9 run function rlk:mboss/arena/ap_oasis/l/lush/9
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 10 run function rlk:mboss/arena/ap_oasis/l/lush/10
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 11 run function rlk:mboss/arena/ap_oasis/l/lush/11
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 12 run function rlk:mboss/arena/ap_oasis/l/lush/12
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 13 run function rlk:mboss/arena/ap_oasis/l/lush/13
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 14 run function rlk:mboss/arena/ap_oasis/l/lush/14
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 15 run function rlk:mboss/arena/ap_oasis/l/lush/15
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 16 run function rlk:mboss/arena/ap_oasis/l/lush/16
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 17 run function rlk:mboss/arena/ap_oasis/l/lush/17
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 18 run function rlk:mboss/arena/ap_oasis/l/lush/18
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 19 run function rlk:mboss/arena/ap_oasis/l/lush/19
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 20 run function rlk:mboss/arena/ap_oasis/l/lush/20
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 21 run function rlk:mboss/arena/ap_oasis/l/lush/21
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 22 run function rlk:mboss/arena/ap_oasis/l/lush/22
execute if data storage rlk:mboss arjob{kind:"look",look:"lush"} if score #arI mb matches 23 run function rlk:mboss/arena/ap_oasis/l/lush/23
