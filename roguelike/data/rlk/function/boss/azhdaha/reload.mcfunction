# Hook reload (@s = body after /reload: every aux entity is gone: the rig parts, hazards, props, markers, orbs,
# shards, proxies). Scores survive; the state is re-derived from them (plan 4.9):
#   intro -> the fight starts; a normal main-slot pattern is cancelled; the cast slot is cancelled; a running
#   service resumes through its reload (the landslide goes on, an absorb finishes at once, the B3 resumes at its
#   frame tick); bg emitters and the B3 special re-make their props (reload hooks); fields are re-made from the
#   table; the proxies respawn and are re-stated; the arena props are re-made; the rig respawns with its looks.
function rlk:boss/azhdaha/ai/consts
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
scoreboard players set #mbNoLeash mb 0
scoreboard players set #azAftN mb 0
scoreboard players set #azAft0 mb 0
scoreboard players set #azAft1 mb 0
scoreboard players set #azAft2 mb 0
scoreboard players set #azAft3 mb 0
scoreboard players set #azAft4 mb 0
scoreboard players set #azAft5 mb 0
scoreboard players set #azAft6 mb 0
scoreboard players set #azAft7 mb 0
scoreboard players set #azAft8 mb 0
scoreboard players set #azAft9 mb 0
scoreboard players set #azAft10 mb 0
scoreboard players set #azAft11 mb 0
scoreboard players set #azAft12 mb 0
scoreboard players set #azAft13 mb 0
scoreboard players set #azAft14 mb 0
scoreboard players set #azAft15 mb 0
function rlk:boss/azhdaha/rig/init
function rlk:boss/azhdaha/rig/spawn
function rlk:boss/azhdaha/look/apply
execute if score #mbSt mb matches 0 run function rlk:boss/azhdaha/intro/done
# (the framework re-spawned the proxies before this hook, cm.md 5.7; px.set survives: re-state the own state)
function rlk:boss/azhdaha/px/restate
function rlk:boss/azhdaha/arena/props
function rlk:boss/azhdaha/arena/look_now
# the main slot: services resume, patterns are cancelled
execute if score #azPat mb matches 1.. run function rlk:boss/azhdaha/p/reload_d
execute if score #azCast mb matches 1.. run function rlk:boss/azhdaha/cast/cancel
execute if score #azBgL mb matches 1.. run function rlk:boss/azhdaha/bg/reload_l
execute if score #azBgT mb matches 1.. run function rlk:boss/azhdaha/bg/reload_t
function rlk:boss/azhdaha/fld/remake
# (FIX STATE-8) the field ambience chains (after() slots die with /reload) restart for the re-made fields
function rlk:boss/azhdaha/p/firefield/reload_fld
function rlk:boss/azhdaha/p/icespike/reload_fld
scoreboard players set #azHudQ mb 1
