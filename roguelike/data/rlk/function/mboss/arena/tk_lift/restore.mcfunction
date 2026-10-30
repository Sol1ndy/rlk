# The stamp of tk_lift is not the default look: the right version in another look -> the look job back to
# "dust"; anything else (no stamp, an old version, a stub) -> a full build.
execute if data storage rlk:mboss {built_tk_lift:"tk_lift@1:abyss"} run return run function rlk:mboss/arena/tk_lift/look/dust
function rlk:mboss/arena/tk_lift/build
