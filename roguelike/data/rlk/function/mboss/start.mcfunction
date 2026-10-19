# @s = the 중간보스 zone marker, at @s (from room/mob_wave, #combat = its zid). Builds the fight in the
# arena and teleports the player. A failed spawn retries 10 ticks later (#spawnT), 3 failures cancel
# the fight without reward. The body holds rlk_zmob from tick 0, so the zone cannot clear early.
# Mid-bosses always fight in the plaza (#mbAr 0); chapter bosses start through mboss/cb/start (AZ-CM).
scoreboard players set #mbAr mb 0
execute in minecraft:overworld unless function rlk:mboss/ar/loaded run return run function rlk:mboss/start_unloaded
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run scoreboard players set #spawnT room 10
execute unless data storage rlk:mboss cur run function rlk:mboss/roll
execute unless data storage rlk:mboss cur run return run function rlk:mboss/start_fail
function rlk:mboss/start_go
