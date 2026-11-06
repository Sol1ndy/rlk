# Entrance prep of apep (@s = the zone marker, at it): a fresh rlk:mboss cprep.apep, the arena forceloaded and its
# sliced build / look restore started (the result is not needed here), then the module's own prep (gate texts, roll).
data remove storage rlk:mboss cprep.apep
execute in minecraft:overworld run function rlk:mboss/ar/ap_oasis/fl_on
execute in minecraft:overworld run function rlk:mboss/ar/ap_oasis/ensure
function rlk:boss/apep/prep
