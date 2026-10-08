# 프롭 f_grass: 지나갈 수 있는 장식. 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:short_grass keep
execute positioned ~1 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:short_grass keep
execute positioned ~-1 ~ ~1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:fern keep
execute positioned ~2 ~ ~2 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:short_grass keep
execute positioned ~0 ~ ~2 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:short_grass keep
execute positioned ~-2 ~ ~-1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:short_grass keep
execute positioned ~1 ~ ~-2 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:fern keep
execute positioned ~3 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:short_grass keep
