# #g mb = a volley group that just landed a hit: its hazards and props stop testing for hits (the strike
# visuals and the flights go on). #mbGrpL remembers it, so a member made later (hz/init, pj/launch) starts harmless:
# one hit per group even when a member is created after the hit (e.g. a burst made at a prop's life end).
# #mbGrpL2 is the same for one-shot hits only: a #hzRearm hazard (a lingering field ticking every 10 t) that lands next
# overwrites #mbGrpL but not #mbGrpL2, so a later member of the earlier one-shot group still starts harmless.
scoreboard players operation #mbGrpL mb = #g mb
execute unless score @s mbHzRA matches 1.. run scoreboard players operation #mbGrpL2 mb = #g mb
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzG = #g mb run scoreboard players set @s mbHzHit 1
# #hzRearm members of the group re-arm together (one hit per re-arm period for the whole group)
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzG = #g mb if score @s mbHzRA matches 1.. run function rlk:mboss/hz/rearm_at
execute as @e[tag=rlk_mb_pj] if score @s mbPjG = #g mb run scoreboard players set @s mbPjHit 1
