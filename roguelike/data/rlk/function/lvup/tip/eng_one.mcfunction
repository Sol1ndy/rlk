$data modify storage rlk:lvpick en set value {name:"$(e)",color:"white"}
$data modify storage rlk:lvpick en merge from storage rlk:engravings registry.$(e)
function rlk:lvup/tip/eng_line with storage rlk:lvpick en
