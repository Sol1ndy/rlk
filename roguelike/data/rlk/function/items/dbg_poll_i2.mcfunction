$data modify storage rlk:dbgt id set from storage rlk:items ids[$(n)]
execute if data storage rlk:dbgt id run function rlk:items/drop with storage rlk:dbgt
