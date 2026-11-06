# (macro arjob) The last slice of a job of fl_ruins: the stamp of the look just built, the sentinel check (a wrong
# sentinel restarts one full build: #arRedo). Outside a run (the dev view) the forceload goes once it is built.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
$data modify storage rlk:mboss built_fl_ruins set value "fl_ruins@1:$(look)"
$data modify storage rlk:mboss look_fl_ruins set value "$(look)"
scoreboard players set #arOk mb 0
execute if block 760 196 8 minecraft:polished_deepslate run scoreboard players set #arOk mb 1
execute if score #arOk mb matches 1 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/fl_ruins/fl_off
execute if score #arOk mb matches 1 run return run scoreboard players set #arRedo mb 0
data remove storage rlk:mboss built_fl_ruins
execute if score #arRedo mb matches 1 run return run scoreboard players set #arRedo mb 0
scoreboard players set #arRedo mb 1
function rlk:mboss/arena/fl_ruins/build
