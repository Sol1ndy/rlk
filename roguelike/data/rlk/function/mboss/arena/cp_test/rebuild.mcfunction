# Dev / test: drop the stamp of cp_test and build it again (a running job of another arena blocks it).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_cp_test
function rlk:mboss/arena/cp_test/build
