# burrow3 #azPT 388
function rlk:boss/azhdaha/b3/special_stop
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/azhdaha/fx/p/emerge_spikes {r:52}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/azhdaha/fx/p/rock_rain {r:60}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/azhdaha/fx/snd/b3_emerge
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/impact/1
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/impact/2
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/impact/3
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/impact/4
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/impact/5
