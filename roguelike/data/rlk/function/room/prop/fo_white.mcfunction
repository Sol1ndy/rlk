# 프롭 fo_white: 지나갈 수 있는 장식(풀 · 꽃). 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:lily_of_the_valley keep
execute positioned ~1 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:oxeye_daisy keep
execute positioned ~0 ~ ~1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:azure_bluet keep
execute positioned ~-1 ~ ~-1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:lily_of_the_valley keep
