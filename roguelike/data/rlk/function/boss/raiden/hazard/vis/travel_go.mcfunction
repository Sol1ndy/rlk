# @s = travelling hazard at rel rdHGo: its still cards (summoned TRAVEL_GAP ticks ago) start their one
# interpolation now (fx_anim in vfx_world, after the hazards).
scoreboard players operation #rdOwner rd = @s rdHId
execute at @s as @e[tag=rlk_rd_trv,distance=..0.05] if score @s rdVId = #rdOwner rd run tag @s add rlk_rd_fxa
