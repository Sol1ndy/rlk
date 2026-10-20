# Idempotent full cleanup: room/clear (map change, run end, death), room/wipe, uninstall, test stop.
# Never teleports the player (callers that end a run move the player themselves).
function rlk:mboss/cleanup_fight
function rlk:mboss/forget
# chapter arenas (AZ-CM): a running job of one ends, then its forceload goes (cb/pp/<id> adds it again at the next
# entrance build); barrier bands
execute if data storage rlk:mboss arjob{aid:"az_cavern"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run function rlk:mboss/ar/az_cavern/fl_off
execute if data storage rlk:mboss arjob{aid:"cp_test"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/fl_off
