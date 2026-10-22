# Idempotent full cleanup: room/clear (map change, run end, death), room/wipe, uninstall, test stop.
# Never teleports the player (callers that end a run move the player themselves).
function rlk:mboss/cleanup_fight
function rlk:mboss/forget
# chapter arenas (AZ-CM): their forceload goes (ar/<aid>/fl_off aborts a running job of that arena first; cb/pp/<id>
# adds the forceload again at the next entrance build); barrier bands
execute in minecraft:overworld run function rlk:mboss/ar/az_cavern/fl_off
execute in minecraft:overworld run function rlk:mboss/ar/ap_oasis/fl_off
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/fl_off
execute in minecraft:overworld run function rlk:mboss/arena/ap_oasis/sweep {y0:201,y1:202}
