# @s boss where it stands. Immune while rdBlink 1.. (combat/apply); she scatters now (the rig hides where it
# stands), relocates at rdBlink 4 and reforms there.
execute if score @s rdBlink matches 1.. run return 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdBlink 1
function rlk:boss/raiden/rig/state/hidden
execute at @s run function rlk:boss/raiden/movement/depart
