# Moves the rlk_hr_anchor marker to chest of the current clip tick (yaw = the boss's). Effects run at / as it. @s = the boss, at its feet.
execute unless entity @e[type=marker,tag=rlk_hr_anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_anchor"]}
execute store result storage rlk:hr rig.q.c int 1 run scoreboard players get @s hrRigC
execute store result storage rlk:hr rig.q.t int 1 run scoreboard players get @s hrRigT
execute if score @s hrRigT matches ..-1 run data modify storage rlk:hr rig.q.t set value 0
data modify storage rlk:hr rig.q.a set value "chest"
function rlk:boss/scarlet/rig/anchor/r/get with storage rlk:hr rig.q
