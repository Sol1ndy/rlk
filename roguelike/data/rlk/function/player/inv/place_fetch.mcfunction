$data modify storage rlk:pf base set from storage rlk:items registry.$(id).item
execute if data storage rlk:pf base run function rlk:player/inv/place_check with storage rlk:pf
