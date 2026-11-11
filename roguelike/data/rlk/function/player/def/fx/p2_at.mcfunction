# 2단계 패링의 접점(p2): 작은 불꽃 0.45칸 + 불티
function rlk:player/def/fx/g/spark {s:1.1}
particle minecraft:dust{color:[1f,0.95f,0.6f],scale:0.6f} ~ ~ ~ 0.12 0.12 0.12 0 4 force @a[tag=player]
particle minecraft:wax_off ~ ~ ~ 0.08 0.08 0.08 1.5 3 force @a[tag=player]
playsound minecraft:block.chain.hit player @a[tag=player] ~ ~ ~ 0.9 1.7
playsound minecraft:block.amethyst_block.hit player @a[tag=player] ~ ~ ~ 0.5 1.9
