# burrow3 #azPT 361
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/azhdaha/fx/p/mound
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/azhdaha/fx/snd/burrow_loop
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run playsound minecraft:entity.ravager.step hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run playsound minecraft:block.gravel.break hostile @a[tag=player] ~ ~ ~ 0.7 0.5 0.23
