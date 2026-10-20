# burrow3 #azPT 58
function rlk:mboss/azhdaha/px/tail_only
scoreboard players set #azBur mb 1
function rlk:mboss/azhdaha/b3/special_start
function rlk:mboss/azhdaha/fx/snd/b3_rise
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/fx/p/mound
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azET mb matches 1 run function rlk:mboss/azhdaha/fx/p/dust_ring/1 {r:30}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azET mb matches 2 run function rlk:mboss/azhdaha/fx/p/dust_ring/2 {r:30}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azET mb matches 3 run function rlk:mboss/azhdaha/fx/p/dust_ring/3 {r:30}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azET mb matches 4 run function rlk:mboss/azhdaha/fx/p/dust_ring/4 {r:30}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azET mb matches 5 run function rlk:mboss/azhdaha/fx/p/dust_ring/5 {r:30}
