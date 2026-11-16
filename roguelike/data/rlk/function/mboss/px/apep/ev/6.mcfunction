# Proxy a_l: live iff in the current state set (#pxS6) and its column top > 0.3 b (#pxU6).
scoreboard players operation #t mb = #pxS6 mb
scoreboard players operation #t mb *= #pxU6 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/apep/on/6
function rlk:mboss/px/apep/off/6
