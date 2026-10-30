# Proxy tail4: live iff in the current state set (#pxS8) and its column top > 0.3 b (#pxU8).
scoreboard players operation #t mb = #pxS8 mb
scoreboard players operation #t mb *= #pxU8 mb
execute if score #t mb matches 1 run return run function rlk:mboss/px/azhdaha/on/8
function rlk:mboss/px/azhdaha/off/8
