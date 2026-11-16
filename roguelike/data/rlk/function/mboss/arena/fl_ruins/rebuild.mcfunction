# Dev / test: drop the stamp of fl_ruins and build it again (a running job of another arena blocks it).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_fl_ruins
function rlk:mboss/arena/fl_ruins/build
