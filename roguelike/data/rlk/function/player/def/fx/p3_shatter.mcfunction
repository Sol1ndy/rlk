# 퍼펙트 패링이 풀리는 6틱(접점): 별빛이 가는 불꽃 줄기 수십 개로 깨져 한 몸 높이쯤 날아간다. 풀림의 강세(round W): 모루(1.6배) +
# 삼지창 "칭" + 유리 + 낮은 "딩"(1.98 kHz); 0틱에 튼 불꽃놀이의 터짐이 이 틱에 겹친다
particle minecraft:electric_spark ~ ~ ~ 0.06 0.06 0.06 1.5 38 force @a[tag=player]
particle minecraft:wax_on ~ ~ ~ 0.05 0.05 0.05 9 10 force @a[tag=player]
particle minecraft:wax_off ~ ~ ~ 0.05 0.05 0.05 7 8 force @a[tag=player]
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 1.2 1.6
playsound minecraft:item.trident.hit_ground player @a[tag=player] ~ ~ ~ 1 1.2
playsound minecraft:block.glass.break player @a[tag=player] ~ ~ ~ 0.5 1.5
playsound minecraft:entity.arrow.hit_player player @a[tag=player] ~ ~ ~ 0.5 0.78
