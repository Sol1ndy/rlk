# Dev / test: drop the stamp of tk_lift and build it again (a running job of another arena blocks it).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_tk_lift
function rlk:mboss/arena/tk_lift/build
