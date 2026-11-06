# Proxy tail_b: live iff in the current state set (#pxS5) and its column top > 0.3 b (#pxU5).
scoreboard players operation #t mb = #pxS5 mb
scoreboard players operation #t mb *= #pxU5 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/apep/on/5
function rlk:mboss/px/apep/off/5
