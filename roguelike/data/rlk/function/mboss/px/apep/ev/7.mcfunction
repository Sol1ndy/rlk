# Proxy b_l: live iff in the current state set (#pxS7) and its column top > 0.3 b (#pxU7).
scoreboard players operation #t mb = #pxS7 mb
scoreboard players operation #t mb *= #pxU7 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/apep/on/7
function rlk:mboss/px/apep/off/7
