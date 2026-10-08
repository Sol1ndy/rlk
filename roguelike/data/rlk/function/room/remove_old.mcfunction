# 예전 버전의 던전 구역(x,z 960~1087) 정리: 그때 깔아 둔 바닥판·방을 비우고 청크 고정 해제. 그 구역을 만든 적이 없으면 아무 일도 없음
execute in minecraft:overworld if loaded 960 199 960 if loaded 1087 199 1087 run fill 960 199 960 1087 199 1087 minecraft:air
execute in minecraft:overworld if loaded 960 199 960 if loaded 1087 199 1087 run fill 960 200 960 1023 205 1023 minecraft:air
execute in minecraft:overworld if loaded 960 199 960 if loaded 1087 199 1087 run fill 960 200 1024 1023 205 1087 minecraft:air
execute in minecraft:overworld if loaded 960 199 960 if loaded 1087 199 1087 run fill 1024 200 960 1087 205 1023 minecraft:air
execute in minecraft:overworld if loaded 960 199 960 if loaded 1087 199 1087 run fill 1024 200 1024 1087 205 1087 minecraft:air
execute in minecraft:overworld run forceload remove 960 960 1087 1087
