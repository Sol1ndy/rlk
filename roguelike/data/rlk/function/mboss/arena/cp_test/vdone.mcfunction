# Verify job of cp_test: the chunks are loaded.
scoreboard players set #mbArBuild mb 0
data remove storage rlk:mboss arjob
execute unless block 540 199 8 minecraft:polished_deepslate run function rlk:mboss/arena/cp_test/build
