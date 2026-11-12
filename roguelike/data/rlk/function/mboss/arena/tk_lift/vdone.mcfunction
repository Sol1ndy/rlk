# Verify job of tk_lift: the chunks are loaded. Outside a run, the forceload goes when nothing is rebuilt.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
execute unless block 640 196 8 minecraft:polished_deepslate run function rlk:mboss/arena/tk_lift/build
execute if score #mbArBuild mb matches 0 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/tk_lift/fl_off
