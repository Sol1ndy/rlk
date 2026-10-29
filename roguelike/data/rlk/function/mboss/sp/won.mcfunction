# @s = the rift's zone marker, at it (as cb/won): gold left in the arena goes to the player, the fight ends, the player
# returns to the rift (sp/ret_rift), the arena forceload goes. Returns 1 when killed (#mbKilled 1), 0 when cancelled.
scoreboard players operation #mbWas mb = #mbOn mb
execute in minecraft:overworld run function rlk:mboss/ar/box_absorb
function rlk:mboss/cleanup_fight
execute unless data storage rlk:mboss ret.x run function rlk:mboss/ret_here
execute if score #mbWas mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/tp_out
execute if score #mbAr mb matches 2 in minecraft:overworld run function rlk:mboss/arena/ap_oasis/sweep {y0:201,y1:202}
execute in minecraft:overworld run function rlk:mboss/ar/fl_off
execute if score #mbKilled mb matches 1 run return run function rlk:mboss/sp/won_kill
function rlk:mboss/sp/won_cancel
return 0
