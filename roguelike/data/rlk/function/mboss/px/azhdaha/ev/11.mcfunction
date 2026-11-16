# Proxy foot_l: live iff in the current state set (#pxS11) and its column top > 0.3 b (#pxU11).
scoreboard players operation #t mb = #pxS11 mb
scoreboard players operation #t mb *= #pxU11 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/azhdaha/on/11
function rlk:mboss/px/azhdaha/off/11
