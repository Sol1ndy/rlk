# The stamp of ap_oasis is not the default look: the right version in another look -> the look job back to
# "withered"; anything else (no stamp, an old version, a stub) -> a full build.
execute if data storage rlk:mboss {built_ap_oasis:"ap_oasis@1:lush"} run return run function rlk:mboss/arena/ap_oasis/look/withered
function rlk:mboss/arena/ap_oasis/build
