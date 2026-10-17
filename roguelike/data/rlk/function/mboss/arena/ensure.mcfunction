# Rebuild the arena when its version string or the centre sentinel block is wrong (cheap check).
# Run in minecraft:overworld; does nothing while the forceloaded chunks are not loaded yet.
execute unless loaded 176 201 -16 run return fail
execute unless loaded 223 201 31 run return fail
execute unless data storage rlk:mboss {built:"plaza@1"} run return run function rlk:mboss/arena/build
execute unless block 200 200 8 minecraft:pink_wool run return run function rlk:mboss/arena/build
return 1
