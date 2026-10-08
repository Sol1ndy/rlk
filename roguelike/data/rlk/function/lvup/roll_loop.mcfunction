execute if score #pkL tmp matches ..0 run return 0
function rlk:lvup/roll_one
execute if data storage rlk:pick pid run data modify storage rlk:lvpick choices append from storage rlk:pick pid
scoreboard players remove #pkL tmp 1
function rlk:lvup/roll_loop
