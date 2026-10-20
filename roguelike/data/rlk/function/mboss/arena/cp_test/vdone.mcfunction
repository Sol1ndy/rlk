# Verify job of cp_test: the chunks are loaded. Outside a run, the forceload goes when nothing is rebuilt.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
execute unless block 540 199 8 minecraft:polished_deepslate run function rlk:mboss/arena/cp_test/build
execute if score #mbArBuild mb matches 0 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/cp_test/fl_off
