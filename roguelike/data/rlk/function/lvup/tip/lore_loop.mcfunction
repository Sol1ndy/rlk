execute unless data storage rlk:lvpick lq[0] run return 0
data modify storage rlk:lvpick tip append value {text:"\n"}
data modify storage rlk:lvpick tip append from storage rlk:lvpick lq[0]
data remove storage rlk:lvpick lq[0]
function rlk:lvup/tip/lore_loop
