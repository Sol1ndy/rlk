# One flight step of the live lance (the per-tick step from the launch); it vanishes on the impact tick.
scoreboard players remove #aq43L mb 1
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p43l,limit=1] at @s run function rlk:mboss/azhdaha/p/icicle/mv with storage rlk:mboss az.p43.v
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p43l,limit=1] run function rlk:mboss/azhdaha/fx/p/icicle_trail
execute if score #aq43L mb matches 0 run kill @e[type=minecraft:item_display,tag=rlk_mb_az_p43l]
execute if score #aq43L mb matches 0 run kill @e[type=minecraft:marker,tag=rlk_mb_az_p43a]
