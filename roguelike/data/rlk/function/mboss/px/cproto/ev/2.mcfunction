# Proxy tail: live iff in the current state set (#pxS2) and its column top > 0.3 b (#pxU2).
scoreboard players operation #t mb = #pxS2 mb
scoreboard players operation #t mb *= #pxU2 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/cproto/on/2
function rlk:mboss/px/cproto/off/2
