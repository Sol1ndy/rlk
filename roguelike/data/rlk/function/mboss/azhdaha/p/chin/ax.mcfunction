# At the impact point, rotated along the crack line: the chin/impact addon point (E 35, call 23).
scoreboard players operation #azCtxGrp mb = #aq1G mb
scoreboard players set #azCtxSide mb 1
scoreboard players set #azCtxPaw mb 1
scoreboard players set #azCtxA0 mb 0
scoreboard players set #azCtxA1 mb 0
scoreboard players set #azCtxT mb 35
function rlk:mboss/azhdaha/x/ctx
execute store result score #azCtxYaw mb run data get entity @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] Rotation[0]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function rlk:mboss/azhdaha/x/chin_impact
