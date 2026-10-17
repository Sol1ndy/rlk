execute at @e[tag=rlk_mb_proto_star,limit=1] run particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.3 0.3 0.15 30 force @a[tag=player]
execute at @e[tag=rlk_mb_proto_star,limit=1] run playsound minecraft:block.amethyst_block.break hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
kill @e[tag=rlk_mb_proto_star]
kill @e[tag=rlk_mb_proto_starv]
scoreboard players set #mbTrueEl mb 3
function rlk:mboss/true_pct {pct:10}
