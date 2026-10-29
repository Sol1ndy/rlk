# From room/remove (in minecraft:overworld): every chapter arena cleared (when loaded), its forceload released; a
# running arena job is aborted first.
execute if score #mbArBuild mb matches 1.. run function rlk:mboss/arena/abort
function rlk:mboss/arena/ap_oasis/sweep {y0:201,y1:202}
function rlk:mboss/arena/az_cavern/clear
function rlk:mboss/ar/az_cavern/fl_off
function rlk:mboss/arena/ap_oasis/clear
function rlk:mboss/ar/ap_oasis/fl_off
function rlk:mboss/arena/tk_lift/clear
function rlk:mboss/ar/tk_lift/fl_off
function rlk:mboss/arena/cp_test/clear
function rlk:mboss/ar/cp_test/fl_off
