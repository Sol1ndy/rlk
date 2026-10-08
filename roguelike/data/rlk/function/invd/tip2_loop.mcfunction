execute unless data storage rlk:lvpick eq2[0] run return 0
data modify storage rlk:lvpick b.e set from storage rlk:lvpick eq2[0]
function rlk:invd/tip2_one with storage rlk:lvpick b
data remove storage rlk:lvpick eq2[0]
function rlk:invd/tip2_loop
