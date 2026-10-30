# From mboss/main while a body exists. Pause (dead / revival / selection screen / no body entity / no tagged
# player) freezes AI, timers, hazards and projectiles; out-of-bounds puts the player back at the arrival spot.
# No tagged player (a disconnect, the tag gone) is a pause too, so the module's pause hook runs (its decals go and
# their redraw is queued for the resume) instead of the fight freezing silently.
# The libraries are scanned only while their activity flag is set (#mbMvOn #mbHzOn #mbPjOn #mbPlOn: set when
# one is created, kept by every live one in its tick, so the scan stops one tick after the last one ends).
execute unless entity @a[tag=player,limit=1] run return run function rlk:mboss/pause_tick
scoreboard players set #mbP mb 0
execute if entity @a[tag=player,scores={dead=1}] run scoreboard players set #mbP mb 1
execute if entity @a[tag=player,scores={rnDie=1..}] run scoreboard players set #mbP mb 1
execute if entity @a[tag=player,scores={pkMode=1..}] run scoreboard players set #mbP mb 1
execute unless entity @e[tag=rlk_body,limit=1] run scoreboard players set #mbP mb 1
execute if score #mbP mb matches 1 run return run function rlk:mboss/pause_tick
execute if score #mbPause mb matches 1 run function rlk:mboss/resume
execute unless score #mbAr mb matches 1.. if score #mbOn mb matches 1 unless entity @a[tag=player,scores={devMode=1}] as @e[tag=rlk_body,limit=1] at @s run function rlk:mboss/ar/plaza/oob
# chapter fights only (AZ-CM, #mbMode 1; a mid-boss tick pays these two checks): the chapter arena's out of bounds,
# the per-tick push request cleared, the lockv ring buffer, proxy clicks (world_cm_pre); after the module tick the
# proxies follow the shown pose, the body push, the music clock (world_cm_post)
execute if score #mbMode mb matches 1 run function rlk:mboss/world_cm_pre
execute if score #mbMvOn mb matches 1 run function rlk:mboss/mv/all
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/body_tick
execute if score #mbMode mb matches 1 run function rlk:mboss/world_cm_post
execute if score #mbHzOn mb matches 1 run function rlk:mboss/hz/all
execute if score #mbPjOn mb matches 1 run function rlk:mboss/pj/all
execute if score #mbPlOn mb matches 1 run function rlk:mboss/pull/all
execute if score #mbSt mb matches 0..1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/bars
function rlk:mboss/line/tick
