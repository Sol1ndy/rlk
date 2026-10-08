execute unless data storage rlk:lvpick iq[0] run return 0
data modify storage rlk:lvpick a.id set from storage rlk:lvpick iq[0]
function rlk:lvup/eng/item with storage rlk:lvpick a
data remove storage rlk:lvpick iq[0]
function rlk:engravings/scan_loop
