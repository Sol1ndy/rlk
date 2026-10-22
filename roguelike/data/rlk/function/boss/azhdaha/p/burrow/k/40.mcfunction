# burrow #azPT 40
function rlk:boss/azhdaha/fx/p/mound
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/dust_ring/1 {r:30}
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/dust_ring/2 {r:30}
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/dust_ring/3 {r:30}
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/dust_ring/4 {r:30}
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/dust_ring/5 {r:30}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] unless entity @e[tag=rlk_body,distance=..20,limit=1] run scoreboard players set #aq9E mb 1
function rlk:boss/azhdaha/fx/snd/burrow_loop
