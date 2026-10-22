# slide #azPT 220
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p20w6] run function rlk:mboss/hz/resize {r:80,r0:35,w:0}
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/dust_ring/1 {r:60}
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/dust_ring/2 {r:60}
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/dust_ring/3 {r:60}
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/dust_ring/4 {r:60}
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/dust_ring/5 {r:60}
function rlk:boss/azhdaha/fx/p/rock_rain {r:120}
