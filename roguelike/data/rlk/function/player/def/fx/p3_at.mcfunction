# 퍼펙트 패링의 접점, 0틱: 작은 불티와 날카로운 쇳소리
function rlk:player/def/fx/g/spark {s:1.3}
particle minecraft:crit ~ ~ ~ 0.15 0.15 0.15 0.5 8 force @a[tag=player]
particle minecraft:electric_spark ~ ~ ~ 0.08 0.08 0.08 0.4 6 force @a[tag=player]
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 0.5 1.8
playsound minecraft:item.trident.hit player @a[tag=player] ~ ~ ~ 0.9 1.4
