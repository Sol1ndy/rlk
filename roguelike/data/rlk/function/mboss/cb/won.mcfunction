# @s = the chapter zone marker, at it. Gold left in the arena goes to the player, the fight ends, the player returns,
# the arena forceload goes (and its barrier band, when the arena entry has sweep). No reward boxes (chapter rewards are
# the kill's gold x15 x chapter and 2 sapphires). Returns 1 when killed (#mbKilled 1), 0 when cancelled (gate back).
scoreboard players operation #mbWas mb = #mbOn mb
execute in minecraft:overworld run function rlk:mboss/ar/box_absorb
function rlk:mboss/cleanup_fight
execute unless data storage rlk:mboss ret.x run function rlk:mboss/ret_here
execute if score #mbWas mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/tp_out
execute in minecraft:overworld run function rlk:mboss/ar/fl_off
execute if score #mbKilled mb matches 1 run return run function rlk:mboss/cb/won_kill
function rlk:mboss/cb/won_cancel
return 0
