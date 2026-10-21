# addon point stomp3/s1 (host side, called at E - 12 = 5; s2.md 10)
scoreboard players operation #azCtxPaw mb = #aq10P mb
scoreboard players operation #azCtxGrp mb = #aq10G1 mb
scoreboard players operation #azCtxSide mb = #azSide mb
scoreboard players set #azCtxT mb 17
function rlk:boss/azhdaha/x/ctx
execute store result score #azCtxYaw mb run data get entity @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] Rotation[0]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function rlk:boss/azhdaha/x/stomp3_s1
