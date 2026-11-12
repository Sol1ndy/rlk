# Dev / test: drop the stamp of ap_oasis and build it again (a running job of another arena blocks it).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_ap_oasis
function rlk:mboss/arena/ap_oasis/build
