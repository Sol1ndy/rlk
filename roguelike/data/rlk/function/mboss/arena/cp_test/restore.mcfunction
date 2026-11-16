# The stamp of cp_test is not the default look: the right version in another look -> the look job back to
# "plain"; anything else (no stamp, an old version, a stub) -> a full build.
execute if data storage rlk:mboss {built_cp_test:"cp_test@1:lit"} run return run function rlk:mboss/arena/cp_test/look/plain
function rlk:mboss/arena/cp_test/build
