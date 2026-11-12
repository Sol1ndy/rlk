# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110; under the ending's lock until E118.
# The first tick without the lock (the framework releases the player in this tick): the stands, the actor and the
# stage go.
function rlk:mboss/cam/kill
function rlk:char/cine/stop
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
scoreboard players set #sq_h hr 0
