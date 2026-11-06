# Proxy foot_r: live iff in the current state set (#pxS12) and its column top > 0.3 b (#pxU12).
scoreboard players operation #t mb = #pxS12 mb
scoreboard players operation #t mb *= #pxU12 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/azhdaha/on/12
function rlk:mboss/px/azhdaha/off/12
