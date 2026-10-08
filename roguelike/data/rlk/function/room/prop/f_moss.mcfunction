# 프롭 f_moss: 지나갈 수 있는 장식. 놓을 자리를 스스로 확인한다
execute positioned ~0 ~ ~0 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:moss_carpet keep
execute positioned ~1 ~ ~0 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:moss_carpet keep
execute positioned ~0 ~ ~1 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:moss_carpet keep
execute positioned ~-1 ~ ~1 unless block ~ ~-1 ~ #rlk:dash_pass run setblock ~ ~ ~ minecraft:moss_carpet keep
