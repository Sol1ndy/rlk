# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110; under the ending's lock until E118.
# Cancel (no executor; idempotent): what this sequence made.
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
function rlk:mboss/cam/kill
function rlk:char/cine/stop
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set #mbCam mb 0
function rlk:boss/scarlet/fx/hud/clear
scoreboard players set @a[tag=player] hudHold 0
kill @e[tag=rlk_hr_ev]
