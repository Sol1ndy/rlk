$data modify storage rlk:io src set from storage rlk:items registry.$(id)
$data modify storage rlk:io id set value "$(id)"
$data modify storage rlk:io slot set value "inventory.$(sl)"
data modify storage rlk:io clickdrop set value 1b
execute if data storage rlk:io src.item run function rlk:items/place_do
