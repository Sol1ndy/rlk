# Dev / test: drop the stamp of az_cavern and build it again (a running job of another arena blocks it).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_az_cavern
function rlk:mboss/arena/az_cavern/build
