# At the landing point (the anchor), rotated toward the player: jump/wave2 (E 32, call 20).
scoreboard players operation #azCtxGrp mb = #aq2G2 mb
scoreboard players set #azCtxSide mb 1
scoreboard players set #azCtxPaw mb 1
scoreboard players set #azCtxA0 mb 0
scoreboard players set #azCtxA1 mb 0
scoreboard players set #azCtxT mb 32
function rlk:boss/azhdaha/x/ctx
execute store result score #azCtxYaw mb run data get entity @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] Rotation[0]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function rlk:boss/azhdaha/x/jump_wave2
