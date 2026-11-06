execute if score #mi tmp > #n tmp run return 0
data modify storage rlk:room mids append value 0
execute store result storage rlk:room mids[-1] int 1 run scoreboard players get #mi tmp
scoreboard players add #mi tmp 1
function rlk:room/node/mids_loop
