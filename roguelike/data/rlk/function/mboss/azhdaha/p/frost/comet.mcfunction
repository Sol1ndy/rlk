# +18: the icicle comet appears high over the circle and dives into its centre in 4 t (the timing cue).
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p41i]
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] run summon minecraft:item_display ~1.5 ~12 ~1.5 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p41","rlk_mb_az_p41i"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p41i,limit=1] run function rlk:mboss/azhdaha/fx/prop/icicle
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p41i,limit=1] at @s if entity @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] facing entity @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p41i,limit=1] run function rlk:mboss/azhdaha/fx/p/icicle_trail
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] run function rlk:mboss/azhdaha/fx/snd/frost_icicle
