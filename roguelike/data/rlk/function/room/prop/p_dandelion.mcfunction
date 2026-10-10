# 프롭 p_dandelion: 지나갈 수 있는 장식(풀 · 꽃). 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:dandelion keep
execute positioned ~1 ~ ~1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:dandelion keep
execute positioned ~-1 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:cornflower keep
execute positioned ~0 ~ ~-2 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:dandelion keep
execute positioned ~2 ~ ~-1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:oxeye_daisy keep
execute positioned ~-2 ~ ~2 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:poppy keep
