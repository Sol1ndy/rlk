# @s = an anchor, at it: open now (the grow finished; /reload during the grow; a reopen): state 2, the hover object.
scoreboard players set @s riftS 2
scoreboard players set @s riftT 0
scoreboard players set @s riftDw 0
function rlk:room/rift/look/open
scoreboard players operation #riftZid room = @s zid
scoreboard players set #riftHas room 0
execute as @e[tag=rlk_rift_obj,type=minecraft:marker] if score @s zid = #riftZid room run scoreboard players set #riftHas room 1
execute if score #riftHas room matches 0 run function rlk:room/obj/k_rift
