# (macro arjob) The last slice of a job of cp_test: the stamp of the look just built, the sentinel check (a wrong
# sentinel restarts one full build: #arRedo). Outside a run (the dev view) the forceload goes once it is built.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
$data modify storage rlk:mboss built_cp_test set value "cp_test@1:$(look)"
scoreboard players set #arOk mb 0
execute if block 540 199 8 minecraft:polished_deepslate run scoreboard players set #arOk mb 1
execute if score #arOk mb matches 1 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/cp_test/fl_off
execute if score #arOk mb matches 1 run return run scoreboard players set #arRedo mb 0
data remove storage rlk:mboss built_cp_test
execute if score #arRedo mb matches 1 run return run scoreboard players set #arRedo mb 0
scoreboard players set #arRedo mb 1
function rlk:mboss/arena/cp_test/build
