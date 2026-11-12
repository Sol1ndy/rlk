# Proxy paw_r: live iff in the current state set (#pxS10) and its column top > 0.3 b (#pxU10).
scoreboard players operation #t mb = #pxS10 mb
scoreboard players operation #t mb *= #pxU10 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/azhdaha/on/10
function rlk:mboss/px/azhdaha/off/10
