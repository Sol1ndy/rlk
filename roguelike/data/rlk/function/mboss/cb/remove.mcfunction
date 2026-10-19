# From room/remove (in minecraft:overworld): every chapter arena cleared (when loaded), its forceload released; a
# running arena job is aborted first.
execute if score #mbArBuild mb matches 1.. run function rlk:mboss/arena/abort
function rlk:mboss/arena/az_cavern/clear
function rlk:mboss/ar/az_cavern/fl_off
function rlk:mboss/arena/cp_test/clear
function rlk:mboss/ar/cp_test/fl_off
