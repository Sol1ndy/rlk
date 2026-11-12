# (macro arjob) The last slice of a job of hr_field: the stamp of the look just built, the sentinel check (a wrong
# sentinel restarts one full build: #arRedo). Outside a run (the dev view) the forceload goes once it is built.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
$data modify storage rlk:mboss built_hr_field set value "hr_field@1:$(look)"
$data modify storage rlk:mboss look_hr_field set value "$(look)"
scoreboard players set #arOk mb 0
execute if block 880 196 8 minecraft:polished_tuff run scoreboard players set #arOk mb 1
execute if score #arOk mb matches 1 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/hr_field/fl_off
execute if score #arOk mb matches 1 run return run scoreboard players set #arRedo mb 0
data remove storage rlk:mboss built_hr_field
execute if score #arRedo mb matches 1 run return run scoreboard players set #arRedo mb 0
scoreboard players set #arRedo mb 1
function rlk:mboss/arena/hr_field/build
