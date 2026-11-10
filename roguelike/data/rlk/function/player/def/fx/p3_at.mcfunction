# 퍼펙트 패링의 접점(p3)
function rlk:player/def/fx/g/star {s:1.25}
particle minecraft:flash{color:[1f,0.93f,0.62f,1f]} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
particle minecraft:crit ~ ~ ~ 0.25 0.25 0.25 0.6 14 force @a[tag=player]
particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.12 8 force @a[tag=player]
particle minecraft:dust{color:[1f,0.78f,0.25f],scale:1.1f} ~ ~ ~ 0.3 0.3 0.3 0 10 force @a[tag=player]
particle minecraft:electric_spark ~ ~ ~ 0.2 0.2 0.2 0.25 8 force @a[tag=player]
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 0.5 1.8
playsound minecraft:item.trident.hit player @a[tag=player] ~ ~ ~ 0.8 1.4
playsound minecraft:block.amethyst_block.resonate player @a[tag=player] ~ ~ ~ 0.8 1.6
