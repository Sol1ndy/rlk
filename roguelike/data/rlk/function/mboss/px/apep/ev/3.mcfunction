# Proxy abd: live iff in the current state set (#pxS3) and its column top > 0.3 b (#pxU3).
scoreboard players operation #t mb = #pxS3 mb
scoreboard players operation #t mb *= #pxU3 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/apep/on/3
function rlk:mboss/px/apep/off/3
