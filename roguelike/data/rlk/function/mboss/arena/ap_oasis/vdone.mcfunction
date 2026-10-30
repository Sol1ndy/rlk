# Verify job of ap_oasis: the chunks are loaded. Outside a run, the forceload goes when nothing is rebuilt.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
execute unless block 440 193 8 minecraft:packed_mud run function rlk:mboss/arena/ap_oasis/build
execute if score #mbArBuild mb matches 0 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/ap_oasis/fl_off
