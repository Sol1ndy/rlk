execute unless data storage rlk:lvpick eq[0] run return 0
data modify storage rlk:lvpick e set from storage rlk:lvpick eq[0]
function rlk:lvup/tip/eng_one with storage rlk:lvpick
data remove storage rlk:lvpick eq[0]
function rlk:lvup/tip/eng_loop
