# @s = the chapter zone marker, at it. Gold left in the arena goes to the player, the fight ends, the player returns,
# the arena forceload goes (and its barrier band, when the arena entry has sweep). No reward boxes (chapter rewards are
# the kill's gold x15 x chapter and 2 sapphires). Returns 1 when killed (#mbKilled 1), 0 when cancelled (gate back).
scoreboard players operation #mbWas mb = #mbOn mb
execute in minecraft:overworld run function rlk:mboss/ar/box_absorb
function rlk:mboss/cleanup_fight
execute unless data storage rlk:mboss ret.x run function rlk:mboss/ret_here
execute if score #mbWas mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/tp_out
# a running job of the fight arena (a module look swap, a rebuild) ends before its forceload goes: without the
# chunks it would only wait, refuse every gate press for 200 t and abort (cm.md 12); ensure restarts it at the next press
execute if score #mbAr mb matches 1 if data storage rlk:mboss arjob{aid:"az_cavern"} run function rlk:mboss/arena/abort
execute if score #mbAr mb matches 9 if data storage rlk:mboss arjob{aid:"cp_test"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run function rlk:mboss/ar/fl_off
execute if score #mbKilled mb matches 1 run return run function rlk:mboss/cb/won_kill
function rlk:mboss/cb/won_cancel
return 0
