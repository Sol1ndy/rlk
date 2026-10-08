$execute unless data storage rlk:lvpick choices[$(h)] run return 0
$data modify storage rlk:lvpick a.id set from storage rlk:lvpick choices[$(h)]
data modify storage rlk:lvpick a.obj set value "engAdd"
function rlk:lvup/eng/item with storage rlk:lvpick a
