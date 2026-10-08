$data modify storage rlk:io engc set value {name:"$(enge)",color:"white"}
$data modify storage rlk:io engc merge from storage rlk:engravings registry.$(enge)
function rlk:items/lore/engr_add with storage rlk:io engc
