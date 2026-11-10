# 2단계 패링의 접점(p2)
function rlk:player/def/fx/g/star {s:0.7}
particle minecraft:flash{color:[1f,0.88f,0.55f,1f]} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.45 8 force @a[tag=player]
particle minecraft:dust{color:[1f,0.8f,0.3f],scale:0.8f} ~ ~ ~ 0.2 0.2 0.2 0 6 force @a[tag=player]
playsound minecraft:item.shield.block player @a[tag=player] ~ ~ ~ 0.8 1.3
playsound minecraft:entity.player.attack.crit player @a[tag=player] ~ ~ ~ 0.6 1.5
