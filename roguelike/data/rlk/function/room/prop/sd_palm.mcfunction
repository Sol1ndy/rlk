# 프롭 sd_palm (위치 = 기준 칸의 땅 바로 위)
setblock ~0 ~0 ~0 minecraft:jungle_log
setblock ~0 ~1 ~0 minecraft:jungle_log
setblock ~0 ~2 ~0 minecraft:jungle_log
setblock ~0 ~3 ~0 minecraft:jungle_log
setblock ~0 ~4 ~0 minecraft:jungle_log
setblock ~0 ~5 ~0 minecraft:jungle_log
setblock ~0 ~6 ~0 minecraft:jungle_log
execute positioned ~0 ~7 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~0 ~8 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~1 ~7 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~2 ~7 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~3 ~6 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~-1 ~7 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~-2 ~7 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~-3 ~6 ~0 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~0 ~7 ~1 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~0 ~7 ~2 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~0 ~6 ~3 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~0 ~7 ~-1 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~0 ~7 ~-2 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~0 ~6 ~-3 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~1 ~7 ~1 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~2 ~6 ~2 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~1 ~7 ~-1 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~2 ~6 ~-2 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~-1 ~7 ~1 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~-2 ~6 ~2 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~-1 ~7 ~-1 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
execute positioned ~-2 ~6 ~-2 if block ~ ~ ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:jungle_leaves[persistent=true]
