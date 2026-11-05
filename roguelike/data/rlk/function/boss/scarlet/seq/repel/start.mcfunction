# CS2 / CS3 repel {at:60|5} (PLAN §3.4): lock, grab, the clash on the hat, the half circle, back to back, the throw, the kick.
# Start (@s = the body, at it; #sq hr = 0) — macro.
$scoreboard players set #sq_at hr $(at)
function rlk:boss/scarlet/rig/face/player
execute positioned as @e[tag=rlk_body,limit=1] run function rlk:mboss/pull/start {t:0}
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/rig/play/repel
scoreboard players set #sqdone hr 0
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/clash_spark
function rlk:boss/scarlet/fx/snd/repel_lock
