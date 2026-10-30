# G2 nova tick (#pat 53).
scoreboard players add #pt tk 1
function rlk:boss/tachy/p/mantle/nova/tick
execute if score #done tk matches 1 run return run function rlk:boss/tachy/mantle/end
execute if score #pt tk matches 104.. run function rlk:boss/tachy/mantle/end
