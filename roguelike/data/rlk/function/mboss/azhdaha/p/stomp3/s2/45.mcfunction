# stomp3 s2 #azPT 45
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p10w2] run function rlk:mboss/hz/resize {r:82,r0:62,w:0}
execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/splash_wall {r:65}
execute unless score #azE mb matches 2 run execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/fx/p/dust_ring/1 {r:65}
execute unless score #azE mb matches 2 run execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/dust_ring/2 {r:65}
execute unless score #azE mb matches 2 run execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/fx/p/dust_ring/3 {r:65}
execute unless score #azE mb matches 2 run execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/fx/p/dust_ring/4 {r:65}
execute unless score #azE mb matches 2 run execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/fx/p/dust_ring/5 {r:65}
