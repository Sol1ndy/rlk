# #g mb = a volley group that just landed a hit: its hazards and props stop testing for hits (the strike
# visuals and the flights go on). #mbGrpL remembers it, so a member made later (hz/init, pj/launch) starts harmless:
# one hit per group even when a member is created after the hit (e.g. a burst made at a prop's life end).
scoreboard players operation #mbGrpL mb = #g mb
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzG = #g mb run scoreboard players set @s mbHzHit 1
execute as @e[tag=rlk_mb_pj] if score @s mbPjG = #g mb run scoreboard players set @s mbPjHit 1
