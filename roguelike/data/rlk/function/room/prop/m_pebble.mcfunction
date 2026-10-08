# 프롭 m_pebble: 지나갈 수 있는 장식. 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:stone_button[face=floor,facing=north] keep
execute positioned ~2 ~ ~1 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:stone_button[face=floor,facing=east] keep
execute positioned ~-1 ~ ~2 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:polished_blackstone_button[face=floor,facing=south] keep
execute positioned ~1 ~ ~-2 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:stone_button[face=floor,facing=west] keep
