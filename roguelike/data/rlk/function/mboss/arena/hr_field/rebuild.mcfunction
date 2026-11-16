# Dev / test: drop the stamp of hr_field and build it again (a running job of another arena blocks it).
execute if score #mbArBuild mb matches 1.. run return fail
data remove storage rlk:mboss built_hr_field
function rlk:mboss/arena/hr_field/build
