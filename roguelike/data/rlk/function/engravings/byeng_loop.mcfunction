execute unless data storage rlk:engravings bq[0] run return 0
data modify storage rlk:engravings bcur set value {}
data modify storage rlk:engravings bcur.id set from storage rlk:engravings bq[0]
function rlk:engravings/byeng_item with storage rlk:engravings bcur
data remove storage rlk:engravings bq[0]
function rlk:engravings/byeng_loop
