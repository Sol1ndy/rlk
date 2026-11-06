# The item (@s = the player): the star raised to 1 before the item is built (by id, held or not), the capacity check
# of F:root/give:4-5 (a full inventory: the drop waits for the rift, #hrEvDrop 1), else items/give.
scoreboard players set #enh tmp 0
function rlk:items/enh_get {id:"sword_hwamu"}
execute if score #enh tmp matches ..0 run function rlk:items/enh_add {id:"sword_hwamu"}
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp >= @s invCap run return run scoreboard players set #hrEvDrop hr 1
function rlk:items/give {id:"sword_hwamu"}
