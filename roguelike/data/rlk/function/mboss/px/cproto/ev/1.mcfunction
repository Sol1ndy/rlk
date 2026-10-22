# Proxy core: live iff in the current state set (#pxS1) and its column top > 0.3 b (#pxU1).
scoreboard players operation #t mb = #pxS1 mb
scoreboard players operation #t mb *= #pxU1 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/cproto/on/1
function rlk:mboss/px/cproto/off/1
