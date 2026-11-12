# Entrance prep of arlecchino (@s = the zone marker, at it): a fresh rlk:mboss cprep.arlecchino, the arena forceloaded and its
# sliced build / look restore started (the result is not needed here), then the module's own prep (gate texts, roll).
data remove storage rlk:mboss cprep.arlecchino
execute in minecraft:overworld run function rlk:mboss/ar/fl_ruins/fl_on
execute in minecraft:overworld run function rlk:mboss/ar/fl_ruins/ensure
function rlk:boss/arlecchino/prep
