# 퍼펙트 패링이 풀리는 6틱(접점): 별빛이 가는 불꽃 줄기 수십 개로 깨져 한 몸 높이쯤 날아간다
particle minecraft:electric_spark ~ ~ ~ 0.06 0.06 0.06 1.5 38 force @a[tag=player]
particle minecraft:wax_on ~ ~ ~ 0.05 0.05 0.05 9 10 force @a[tag=player]
particle minecraft:wax_off ~ ~ ~ 0.05 0.05 0.05 7 8 force @a[tag=player]
playsound minecraft:block.glass.break player @a[tag=player] ~ ~ ~ 0.4 1.8
playsound minecraft:entity.firework_rocket.twinkle player @a[tag=player] ~ ~ ~ 0.5 1.5
