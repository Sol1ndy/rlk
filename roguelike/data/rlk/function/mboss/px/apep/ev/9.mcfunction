# Proxy b_r: live iff in the current state set (#pxS9) and its column top > 0.3 b (#pxU9).
scoreboard players operation #t mb = #pxS9 mb
scoreboard players operation #t mb *= #pxU9 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/apep/on/9
function rlk:mboss/px/apep/off/9
