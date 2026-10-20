# tailslam #azPT 39
function rlk:mboss/azhdaha/fx/snd/tslam_impact
execute positioned ^0 ^0 ^-4.75 rotated ~180 0 run function rlk:mboss/azhdaha/fx/p/tail_lane
execute positioned ^0 ^0 ^-4.75 rotated ~180 0 run execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/fx/p/dust_ring/1 {r:25}
execute positioned ^0 ^0 ^-4.75 rotated ~180 0 run execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/dust_ring/2 {r:25}
execute positioned ^0 ^0 ^-4.75 rotated ~180 0 run execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/fx/p/dust_ring/3 {r:25}
execute positioned ^0 ^0 ^-4.75 rotated ~180 0 run execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/fx/p/dust_ring/4 {r:25}
execute positioned ^0 ^0 ^-4.75 rotated ~180 0 run execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/fx/p/dust_ring/5 {r:25}
execute positioned ^0 ^0 ^-11.25 run execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/fx/p/impact/1
execute positioned ^0 ^0 ^-11.25 run execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/impact/2
execute positioned ^0 ^0 ^-11.25 run execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/fx/p/impact/3
execute positioned ^0 ^0 ^-11.25 run execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/fx/p/impact/4
execute positioned ^0 ^0 ^-11.25 run execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/fx/p/impact/5
execute positioned ^0 ^0 ^-16.75 run function rlk:mboss/azhdaha/fx/p/leaf_burst
