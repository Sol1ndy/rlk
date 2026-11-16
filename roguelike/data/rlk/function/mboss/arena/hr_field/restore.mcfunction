# The stamp of hr_field is not the default look: the right version in another look -> the look job back to
# "moon"; anything else (no stamp, an old version, a stub) -> a full build.
execute if data storage rlk:mboss {built_hr_field:"hr_field@1:crimson"} run return run function rlk:mboss/arena/hr_field/look/moon
execute if data storage rlk:mboss {built_hr_field:"hr_field@1:dark"} run return run function rlk:mboss/arena/hr_field/look/moon
function rlk:mboss/arena/hr_field/build
