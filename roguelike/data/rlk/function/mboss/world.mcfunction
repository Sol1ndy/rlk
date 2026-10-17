# From rlk:tick while a body exists. Pause (dead / revival / selection screen / no body entity) freezes
# AI, timers, hazards and projectiles; out-of-bounds puts the player back at the arrival spot.
execute unless entity @a[tag=player,limit=1] run return 0
scoreboard players set #mbP mb 0
execute if entity @a[tag=player,scores={dead=1}] run scoreboard players set #mbP mb 1
execute if entity @a[tag=player,scores={rnDie=1..}] run scoreboard players set #mbP mb 1
execute if entity @a[tag=player,scores={pkMode=1..}] run scoreboard players set #mbP mb 1
execute unless entity @e[tag=rlk_body,limit=1] run scoreboard players set #mbP mb 1
execute if score #mbP mb matches 1 run return run function rlk:mboss/pause_tick
execute if score #mbPause mb matches 1 run function rlk:mboss/resume
execute if score #mbOn mb matches 1 unless entity @a[tag=player,scores={devMode=1}] as @e[tag=rlk_body,limit=1] at @s run function rlk:mboss/oob
execute if entity @e[tag=rlk_mb_mv,limit=1] as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/tick
execute as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/body_tick
execute if entity @e[tag=rlk_mb_hz,limit=1] as @e[tag=rlk_mb_hz] at @s rotated as @s run function rlk:mboss/hz/tick
execute if entity @e[tag=rlk_mb_pj,limit=1] as @e[tag=rlk_mb_pj] at @s rotated as @s run function rlk:mboss/pj/tick
execute if entity @e[tag=rlk_mb_pullpt,limit=1] as @e[tag=rlk_mb_pullpt] at @s run function rlk:mboss/pull/tick
execute if score #mbSt mb matches 0..1 as @e[tag=rlk_mb_body,limit=1] run function rlk:mboss/bars
function rlk:mboss/line/tick
