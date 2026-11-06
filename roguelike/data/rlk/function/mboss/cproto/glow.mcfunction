# Every 10 t while the entrance glyph prop exists (room/clear kills it; uninstall clears the schedule): a soft glow.
execute unless entity @e[tag=rlk_mb_cproto_glyph,limit=1] run return 0
execute at @e[tag=rlk_mb_cproto_glyph,limit=1] run particle minecraft:end_rod ~ ~0.2 ~ 0.15 0.2 0.15 0.01 2
schedule function rlk:mboss/cproto/glow 10t replace
