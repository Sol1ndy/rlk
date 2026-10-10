# 프롭 p_litter: 지나갈 수 있는 장식(풀 · 꽃). 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:leaf_litter[segment_amount=4] keep
execute positioned ~1 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:leaf_litter[segment_amount=3,facing=east] keep
execute positioned ~0 ~ ~1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:leaf_litter[segment_amount=2,facing=south] keep
