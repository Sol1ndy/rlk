# 1단계 패링의 접점(p1): 작은 불꽃 0.3칸
function rlk:player/def/fx/g/spark {s:0.75}
particle minecraft:dust{color:[1f,0.95f,0.6f],scale:0.5f} ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[tag=player]
playsound minecraft:block.chain.hit player @a[tag=player] ~ ~ ~ 0.8 1.25
