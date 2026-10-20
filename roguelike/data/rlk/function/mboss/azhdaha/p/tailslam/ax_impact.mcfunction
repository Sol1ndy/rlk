# addon point tailslam/impact (host side, called at E - 12 = 27; s2.md 10)
scoreboard players operation #azCtxGrp mb = #aq8G mb
scoreboard players set #azCtxT mb 39
scoreboard players operation #azCtxSide mb = #azSide mb
function rlk:mboss/azhdaha/x/ctx
execute store result score #azCtxYaw mb run data get entity @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] Rotation[0]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function rlk:mboss/azhdaha/x/tailslam_impact
