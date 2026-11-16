# Proxy hips: live iff in the current state set (#pxS4) and its column top > 0.3 b (#pxU4).
scoreboard players operation #t mb = #pxS4 mb
scoreboard players operation #t mb *= #pxU4 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/azhdaha/on/4
function rlk:mboss/px/azhdaha/off/4
