# 퍼펙트 패링의 별빛, 2틱(접점): 한 번에 다 큰 크기(1.3칸 ≈ 몸 높이의 0.7), 멈춘 동안 그대로. 밝고 긴 울림
function rlk:player/def/fx/g/star {s:1.1}
particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.02 4 force @a[tag=player]
playsound minecraft:block.amethyst_block.resonate player @a[tag=player] ~ ~ ~ 0.9 1.6
playsound minecraft:block.amethyst_block.chime player @a[tag=player] ~ ~ ~ 0.8 1.25
playsound minecraft:block.bell.resonate player @a[tag=player] ~ ~ ~ 0.35 2
