$data modify storage rlk:room t set from storage rlk:room types[$(t)]
scoreboard players set #oact tmp 7
function rlk:room/obj/make_item with storage rlk:room t
