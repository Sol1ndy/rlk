scoreboard players set #pst tmp 3
function rlk:cm/cn/sim_s
execute if score #sdone tmp matches 1 run return 0
scoreboard players remove #svy tmp 30
scoreboard players remove #sn tmp 1
execute if score #sn tmp matches 1.. run function rlk:cm/cn/sim_t
