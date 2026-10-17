# @s = the 중간보스 zone marker, at @s (from room/mob_wave, #combat = its zid). Builds the fight in the
# arena and teleports the player. A failed spawn retries 10 ticks later (#spawnT), 3 failures cancel
# the fight without reward. The body holds rlk_zmob from tick 0, so the zone cannot clear early.
execute in minecraft:overworld unless loaded 200 201 8 run return run function rlk:mboss/start_unloaded
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run scoreboard players set #spawnT room 10
execute unless data storage rlk:mboss cur run function rlk:mboss/roll
execute unless data storage rlk:mboss cur run return run function rlk:mboss/start_fail
scoreboard players set #mbLd mb 0
# From here on fight entities may exist: rlk:tick runs mboss/main (cleared when the body is gone).
scoreboard players set #mbLive mb 1
function rlk:mboss/cleanup_aux
function rlk:mboss/fight_vars
execute in minecraft:overworld run function rlk:mboss/arena/ensure
execute in minecraft:overworld run summon minecraft:marker 200 201 8 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_arena"],Rotation:[180.0f,0.0f]}
execute in minecraft:overworld as @e[tag=rlk_mb_arena,limit=1] at @s rotated as @s run function rlk:mboss/d/spawn
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run function rlk:mboss/start_fail
scoreboard players set #mbFail mb 0
function rlk:mboss/ret_save
scoreboard players operation #mbLv mb = @e[tag=rlk_mb_body,limit=1] mlv
data modify storage rlk:mboss met append from storage rlk:mboss cur.id
scoreboard players set #mbOn mb 1
scoreboard players set #mbSt mb 0
scoreboard players set #mbT mb 0
execute as @a[tag=player,limit=1] run function rlk:mboss/tp_in
function rlk:mboss/bars_show
