# addon point whip/sweep (host side, called at E - 12 = 11; s2.md 10)
scoreboard players operation #azCtxSide mb = #aq7S mb
scoreboard players operation #azCtxGrp mb = #aq7G mb
scoreboard players set #azCtxT mb 23
scoreboard players operation #azCtxYaw mb = #aq7Y mb
scoreboard players operation #azCtxA0 mb = #aq7Y mb
scoreboard players remove #azCtxA0 mb 179
scoreboard players operation #azCtxA1 mb = #aq7Y mb
scoreboard players remove #azCtxA1 mb 293
function rlk:boss/azhdaha/x/ctx
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function rlk:boss/azhdaha/x/whip_sweep
