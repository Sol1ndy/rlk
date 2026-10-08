data modify storage rlk:room t set from storage rlk:room types[8]
scoreboard players set #oact tmp 7
scoreboard players set #oarg tmp 8
function rlk:room/obj/make_item with storage rlk:room t
