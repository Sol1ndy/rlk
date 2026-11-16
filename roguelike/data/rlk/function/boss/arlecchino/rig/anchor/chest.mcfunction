# Moves the rlk_kn_anchor marker to chest of the current clip tick (yaw = the boss's). Effects run at / as it. @s = the boss, at its feet.
execute unless entity @e[type=marker,tag=rlk_kn_anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_anchor"]}
execute store result storage rlk:kn rig.q.c int 1 run scoreboard players get @s knRigC
execute store result storage rlk:kn rig.q.t int 1 run scoreboard players get @s knRigT
execute if score @s knRigT matches ..-1 run data modify storage rlk:kn rig.q.t set value 0
data modify storage rlk:kn rig.q.a set value "chest"
function rlk:boss/arlecchino/rig/anchor/r/get with storage rlk:kn rig.q
