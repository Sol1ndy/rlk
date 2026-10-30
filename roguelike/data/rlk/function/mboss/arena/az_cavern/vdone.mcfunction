# Verify job of az_cavern: the chunks are loaded. Outside a run, the forceload goes when nothing is rebuilt.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
execute unless block 320 195 8 minecraft:smooth_basalt run function rlk:mboss/arena/az_cavern/build
execute if score #mbArBuild mb matches 0 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/az_cavern/fl_off
