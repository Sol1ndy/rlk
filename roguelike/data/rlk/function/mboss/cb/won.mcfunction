# @s = the chapter zone marker, at it. Gold left in the arena goes to the player, the fight ends, the player returns,
# the arena forceload goes (and its barrier band, when the arena entry has sweep). No reward boxes (chapter rewards are
# the kill's gold x15 x chapter and 2 sapphires). Returns 1 when killed (#mbKilled 1), 0 when cancelled (gate back).
scoreboard players operation #mbWas mb = #mbOn mb
execute in minecraft:overworld run function rlk:mboss/ar/box_absorb
function rlk:mboss/cleanup_fight
execute unless data storage rlk:mboss ret.x run function rlk:mboss/ret_here
execute if score #mbWas mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/tp_out
execute if score #mbAr mb matches 2 in minecraft:overworld run function rlk:mboss/arena/ap_oasis/sweep {y0:201,y1:202}
# the forceload goes; ar/<aid>/fl_off first aborts a running job of the fight arena (a module look swap, a rebuild:
# without the chunks it would only wait and refuse every gate press for 200 t; cm.md 12); ensure restarts it at the
# next press
execute in minecraft:overworld run function rlk:mboss/ar/fl_off
execute if score #mbKilled mb matches 1 run return run function rlk:mboss/cb/won_kill
function rlk:mboss/cb/won_cancel
return 0
