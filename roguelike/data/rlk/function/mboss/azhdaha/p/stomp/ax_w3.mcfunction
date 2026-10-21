# addon point stomp/w3 (host side, called at E - 12 = 35; s2.md 10)
scoreboard players operation #azCtxPaw mb = #aq5P mb
scoreboard players operation #azCtxGrp mb = #aq5G3 mb
scoreboard players operation #azCtxSide mb = #azSide mb
scoreboard players set #azCtxT mb 47
function rlk:mboss/azhdaha/x/ctx
execute store result score #azCtxYaw mb run data get entity @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] Rotation[0]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function rlk:mboss/azhdaha/x/stomp_w3
