# Verify job of hr_field: the chunks are loaded. Outside a run, the forceload goes when nothing is rebuilt.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
execute unless block 880 196 8 minecraft:polished_tuff run function rlk:mboss/arena/hr_field/build
execute if score #mbArBuild mb matches 0 unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/hr_field/fl_off
