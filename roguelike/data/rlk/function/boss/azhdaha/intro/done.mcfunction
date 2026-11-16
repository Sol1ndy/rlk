# The intro is over: targetable, the proxies on, phase 1 (Geo, floor F1), the AI after a short cooldown.
function rlk:mboss/intro_end
function rlk:boss/azhdaha/px/normal
function rlk:boss/azhdaha/svc/phase_1
scoreboard players set #azCool mb 20
scoreboard players set #azHudQ mb 1
# (FIX STATE-7) an intro cut before its roar (/reload, test 99) still starts the phase-1 track
execute unless score #mbMusPh mb matches 1.. run function rlk:boss/azhdaha/svc/music_1
