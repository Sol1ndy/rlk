# F3 (HR-33): the item's stars as the item itself shows them (F:items/build_display: rlk:items stars[<its star>], the
# colours of F:items/register read at run time) -> storage ev.sx, for the coda title and the chat record. The star is
# the item's own (rlk:pinv enh, raised to api.EVENT item_enh by ev/item before; 0-3).
scoreboard players set #enh tmp 0
function rlk:items/enh_get {id:"sword_hwamu"}
data modify storage rlk:hr ev.sx set from storage rlk:items stars[0]
execute if score #enh tmp matches 1 run data modify storage rlk:hr ev.sx set from storage rlk:items stars[1]
execute if score #enh tmp matches 2 run data modify storage rlk:hr ev.sx set from storage rlk:items stars[2]
execute if score #enh tmp matches 3.. run data modify storage rlk:hr ev.sx set from storage rlk:items stars[3]
