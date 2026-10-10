# 프롭 sd_bush: 지나갈 수 있는 장식(풀 · 꽃). 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 if block ~ ~-1 ~ #minecraft:sand run setblock ~ ~ ~ minecraft:dead_bush keep
execute positioned ~2 ~ ~1 if block ~ ~-1 ~ #minecraft:sand run setblock ~ ~ ~ minecraft:short_dry_grass keep
execute positioned ~-1 ~ ~-1 if block ~ ~-1 ~ #minecraft:sand run setblock ~ ~ ~ minecraft:dead_bush keep
