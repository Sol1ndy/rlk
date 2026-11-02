# The stamp of fl_ruins is not the default look: the right version in another look -> the look job back to
# "day"; anything else (no stamp, an old version, a stub) -> a full build.
execute if data storage rlk:mboss {built_fl_ruins:"fl_ruins@1:crimson"} run return run function rlk:mboss/arena/fl_ruins/look/day
function rlk:mboss/arena/fl_ruins/build
