# jump l at tick 21 (positioned / rotated at rlk_mb_az_p2l)
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/impact/1
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/impact/2
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/impact/3
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/impact/4
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/impact/5
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/dust_ring/1 {r:45}
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/dust_ring/2 {r:45}
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/dust_ring/3 {r:45}
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/dust_ring/4 {r:45}
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/dust_ring/5 {r:45}
function rlk:boss/azhdaha/fx/snd/jump_land
