# flyslam clip tick 47
execute at @s rotated as @s rotated ~ 0 rotated ~256.528 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^1.707",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:0.546,s1:0.78,move:"0f,0f,0f",life:30,fade:6}
execute at @s rotated as @s rotated ~ 0 rotated ~256.528 0 positioned ^ ^0.2 ^1.707 run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~ ~ 0.2 0.1 0.2 0.1 4 force @a[tag=player]
playsound minecraft:block.pointed_dripstone.land hostile @a[tag=player] ~ ~ ~ 1 1 0.33
playsound minecraft:block.amethyst_cluster.place hostile @a[tag=player] ~ ~ ~ 1 1 0.33
