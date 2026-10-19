# Entrance prep of cproto (@s = the zone marker, at it): a fresh rlk:mboss cprep.cproto, the arena forceloaded and its
# sliced build / look restore started (the result is not needed here), then the module's own prep (gate texts, roll).
data remove storage rlk:mboss cprep.cproto
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/fl_on
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/ensure
function rlk:mboss/cproto/prep
