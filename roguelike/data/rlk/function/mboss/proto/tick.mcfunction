# Hook tick (@s = body, at @s, fight state): rig, hit flash, stars, then idle or the running pattern.
function rlk:mboss/proto/rig/follow
execute if score #prFlash mb matches 1.. run scoreboard players remove #prFlash mb 1
execute if score #prFlash mb matches 0 run function rlk:mboss/proto/rig/unglow
execute if score #prFlash mb matches 0 run scoreboard players set #prFlash mb -1
execute if entity @e[tag=rlk_mb_proto_starv,limit=1] run function rlk:mboss/proto/star_tick
# A star break can be lethal (true_pct runs death_start before it returns): no fight logic on a dying body.
execute unless score #mbSt mb matches 1 run return 0
execute if score #prPat mb matches 0 run return run function rlk:mboss/proto/idle
function rlk:mboss/proto/pattern
