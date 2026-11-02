# Verify job of fl_ruins: the chunks are loaded. Outside a run, the forceload goes when nothing is rebuilt.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
execute unless block 760 196 8 minecraft:polished_deepslate run function rlk:mboss/arena/fl_ruins/build
execute if score #mbArBuild mb matches 0 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/fl_ruins/fl_off
