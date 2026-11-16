# (macro arjob) The last slice of a job of tk_lift: the stamp of the look just built, the sentinel check (a wrong
# sentinel restarts one full build: #arRedo). Outside a run (the dev view) the forceload goes once it is built.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
$data modify storage rlk:mboss built_tk_lift set value "tk_lift@1:$(look)"
$data modify storage rlk:mboss look_tk_lift set value "$(look)"
scoreboard players set #arOk mb 0
execute if block 640 196 8 minecraft:polished_deepslate run scoreboard players set #arOk mb 1
execute if score #arOk mb matches 1 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/tk_lift/fl_off
execute if score #arOk mb matches 1 run return run scoreboard players set #arRedo mb 0
data remove storage rlk:mboss built_tk_lift
execute if score #arRedo mb matches 1 run return run scoreboard players set #arRedo mb 0
scoreboard players set #arRedo mb 1
function rlk:mboss/arena/tk_lift/build
