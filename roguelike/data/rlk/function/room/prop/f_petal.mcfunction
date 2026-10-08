# 프롭 f_petal: 지나갈 수 있는 장식. 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:pink_petals[flower_amount=3] keep
execute positioned ~1 ~ ~0 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:pink_petals[flower_amount=2,facing=east] keep
execute positioned ~0 ~ ~1 if block ~ ~-1 ~ #minecraft:supports_vegetation run setblock ~ ~ ~ minecraft:pink_petals[flower_amount=4,facing=south] keep
